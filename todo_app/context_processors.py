from django.utils import timezone
from .models import Task, UserProfile

def task_info(request):
    if request.user.is_authenticated:
        today = timezone.now().date()
        tasks = Task.objects.filter(user=request.user, created_at__date=today)
        daily_limit = request.user.userprofile.daily_task_limit
        tasks_left_today = daily_limit - tasks.count()

        return {
            'tasks_left_today': tasks_left_today,
            'daily_task_limit': daily_limit,
            'current_gems': request.user.userprofile.gems,
        }
    return {}
