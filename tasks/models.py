from django.utils import timezone
from django.db import models
from django_cte import CTEManager

# Create your models here.
class Task(models.Model):
    # objects = CTEManager()
    title = models.CharField(max_length=100, blank=True)
    desired_weekly_frequency = models.IntegerField(default=7)
    created_at = models.DateTimeField(default=timezone.now)


class TaskCompletions(models.Model):
    # objects = CTEManager()
    task_id = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)
