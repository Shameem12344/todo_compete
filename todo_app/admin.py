from django.contrib import admin
from .models import Task, UserProfile, ShopItem, Purchase ,User

# Register your models here.
admin.site.register(User)
admin.site.register(Task)
admin.site.register(UserProfile)
admin.site.register(ShopItem)
admin.site.register(Purchase)
