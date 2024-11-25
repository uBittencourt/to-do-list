from django.utils import timezone
from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=100, blank=True)
    desired_weekly_frequency = models.IntegerField(default=7)
    created_at = models.DateTimeField(default=timezone.now)


class TaskCompletions(models.Model):
    task_id = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)
