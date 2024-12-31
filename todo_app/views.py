from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator
from .models import User, Task, UserProfile, ShopItem, Purchase, Group
from datetime import datetime
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum

def index(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    else:
        return HttpResponseRedirect(reverse("login"))

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "todo_app/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "todo_app/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "todo_app/register.html", {
                "message": "Passwords must match."
            })

        try:
            with transaction.atomic():
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
            return HttpResponseRedirect(reverse("index"))
        except IntegrityError:
            return render(request, "todo_app/register.html", {
                "message": "Username already taken. Please choose a different username."
            })
        except Exception as e:
            return render(request, "todo_app/register.html", {
                "message": f"An unexpected error occurred: {str(e)}"
            })
    else:
        return render(request, "todo_app/register.html")

@login_required
def task_list(request):
    today = timezone.now().date()
    tasks = Task.objects.filter(user=request.user, created_at__date=today)
    daily_limit = request.user.userprofile.daily_task_limit
    tasks_left_today = daily_limit - tasks.count()

    if request.method == 'POST':
        if 'title' in request.POST:
            if tasks.count() < daily_limit:
                Task.objects.create(user=request.user, title=request.POST['title'])
            else:
                messages.error(request, f"You've reached your daily task limit of {daily_limit}. Visit the shop to increase your limit!")
        elif 'task_id' in request.POST:
            task = Task.objects.get(id=request.POST['task_id'], user=request.user)
            task.completed = True
            task.completion_date = today
            task.save()
            profile = request.user.userprofile
            profile.add_gems(1)  # This method updates both current_gems and all_time_gems
        return redirect('task_list')

    return render(request, 'todo_app/task_list.html', {
        'tasks': tasks,
        'tasks_left_today': tasks_left_today,
        'daily_task_limit': daily_limit,
        'current_group': request.user.userprofile.current_group,
    })

@login_required
def profile_view(request, username):
    user = User.objects.get(username=username)
    today = timezone.now().date()
    completed_tasks = Task.objects.filter(user=user, completed=True).order_by('-completion_date')
    pending_tasks_today = Task.objects.filter(user=user, completed=False, created_at__date=today)
    all_tasks_today = Task.objects.filter(user=user, created_at__date=today)
    tasks_left_today = user.userprofile.daily_task_limit - all_tasks_today.count()
    paginator = Paginator(completed_tasks, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # This Groups tasks by date
    grouped_tasks = {}
    for task in completed_tasks:
        date = task.completion_date
        if date not in grouped_tasks:
            grouped_tasks[date] = {'completed': [], 'pending': []}
        grouped_tasks[date]['completed'].append(task)

    for task in pending_tasks_today:
        date = task.created_at.date()
        if date not in grouped_tasks:
            grouped_tasks[date] = {'completed': [], 'pending': []}
        grouped_tasks[date]['pending'].append(task)

    return render(request, 'todo_app/profile.html', {
        'profile_user': user,
        'grouped_tasks': grouped_tasks,
        'tasks_left_today': tasks_left_today,
        'current_gems': user.userprofile.gems,
        'all_time_gems': user.userprofile.all_time_gems,
        'page_obj': page_obj,
        'daily_task_limit': user.userprofile.daily_task_limit,
        'current_group': user.userprofile.current_group,

    })

@login_required
def tasks_by_date(request, username, date):
    user = User.objects.get(username=username)
    date = datetime.strptime(date, '%Y-%m-%d').date()
    completed_tasks = Task.objects.filter(user=user, completion_date=date, completed=True)
    pending_tasks = Task.objects.filter(user=user, created_at__date=date, completed=False)

    return render(request, 'todo_app/tasks_by_date.html', {
        'profile_user': user,
        'date': date,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
    })

@login_required
def leaderboard(request):
    all_profiles = UserProfile.objects.all().order_by('-all_time_gems')
    paginator = Paginator(all_profiles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "todo_app/leaderboard.html", {
        "leaderboard_data": page_obj,
        "page_obj": page_obj,
        "show_group_leaderboard": True,
    })


@login_required
def shop(request):
    items = ShopItem.objects.all()
    user_profile = request.user.userprofile

    item_prices = {}
    for item in items:
        if item.effect == 'increase_task_limit':
            item_prices[item.id] = user_profile.get_next_task_limit_price()
        else:
            item_prices[item.id] = item.price

    return render(request, 'todo_app/shop.html', {
        'items': items,
        'item_prices': item_prices,
        'in_group': request.user.userprofile.current_group is not None,
    })

@login_required
@transaction.atomic
def purchase_item(request, item_id):
    item = get_object_or_404(ShopItem, id=item_id)
    user_profile = request.user.userprofile

    if user_profile.spend_gems(item.price):  
        Purchase.objects.create(user=request.user, item=item)
        messages.success(request, f'You have successfully purchased {item.name}!')
    else:
        messages.error(request, 'You do not have enough gems to purchase this item.')

    return redirect('shop')

@login_required
def create_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        group = Group.objects.create(name=name, description=description, creator=request.user)
        group.members.add(request.user)
        request.user.userprofile.current_group = group
        request.user.userprofile.save()
        return redirect('group_detail', group_id=group.id)
    return render(request, 'todo_app/create_group.html')

@login_required
def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user not in group.members.all():
        group.members.add(request.user)
        request.user.userprofile.current_group = group
        request.user.userprofile.save()
    return redirect('group_detail', group_id=group.id)

@login_required
def leave_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user in group.members.all():
        group.members.remove(request.user)
        request.user.userprofile.current_group = None
        request.user.userprofile.save()
    return redirect('group_list')

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'todo_app/group_detail.html', {'group': group})

@login_required
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'todo_app/group_list.html', {'groups': groups})

@login_required
def group_leaderboard(request):
    groups = Group.objects.all()
    groups_with_gems = []

    for group in groups:
        total_gems = group.members.aggregate(total=Sum('userprofile__all_time_gems'))['total'] or 0
        groups_with_gems.append({
            'group': group,
            'total_gems': total_gems,
            'members_count': group.members.count()
        })

    # Sort the groups by total gems
    groups_with_gems = sorted(groups_with_gems, key=lambda x: x['total_gems'], reverse=True)

    # Pagination
    paginator = Paginator(groups_with_gems, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'todo_app/group_leaderboard.html', {
        'groups': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages()
    })
