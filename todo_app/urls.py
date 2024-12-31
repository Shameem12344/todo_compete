from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('tasks', views.task_list, name='task_list'),
    path('profile/<str:username>', views.profile_view, name='profile'),
    path('tasks_by_date/<str:username>/<str:date>', views.tasks_by_date, name='tasks_by_date'),
    path('leaderboard', views.leaderboard, name='leaderboard'),
    path('shop/', views.shop, name='shop'),
    path('purchase/<int:item_id>/', views.purchase_item, name='purchase_item'),

# Group related Urls
    path('groups/', views.group_list, name='group_list'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('groups/<int:group_id>/join/', views.join_group, name='join_group'),
    path('groups/<int:group_id>/leave/', views.leave_group, name='leave_group'),
    path('groups/leaderboard/', views.group_leaderboard, name='group_leaderboard'),
]

