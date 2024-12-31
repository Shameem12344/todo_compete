from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Sum

class User(AbstractUser):
    pass

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.completed and not self.completion_date:
            self.completion_date = timezone.now().date()
        super().save(*args, **kwargs)

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(User, related_name='joined_groups')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def total_gems(self):
        return self.members.aggregate(total=Sum('userprofile__all_time_gems'))['total'] or 0


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gems = models.IntegerField(default=0)  # This represents current gems
    all_time_gems = models.IntegerField(default=0)  # This reperesents the all time gems
    daily_task_limit = models.IntegerField(default=5)
    task_limit_increases = models.IntegerField(default=0)
    current_group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_members')

    # This Signals to create a UserProfile when a new User is created

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()

    def get_next_task_limit_price(self):
        base_price = 3
        return base_price + (self.task_limit_increases * 2)

    def increase_task_limit(self):
        self.daily_task_limit += 1
        self.task_limit_increases += 1
        self.save()

    def add_gems(self, amount):
        self.gems += amount
        self.all_time_gems += amount
        self.save()

    def spend_gems(self, amount):
        if self.gems >= amount:
            self.gems -= amount
            self.save()
            return True
        return False
class ShopItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    effect = models.CharField(max_length=100)  # for example increase_task_limit which is the only effect that I have incorporated in the shop so far

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(ShopItem, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=Purchase)
def apply_purchase_effect(sender, instance, created, **kwargs):
    if created:
        if instance.item.effect == 'increase_task_limit':
            instance.user.userprofile.daily_task_limit += 1
            instance.user.userprofile.save()
