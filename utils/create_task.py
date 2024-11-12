import os
import sys
import django
from pathlib import Path
from django.conf import settings

DJANGO_BASE_DIR = Path(__file__).parent.parent

sys.path.append(str(DJANGO_BASE_DIR))
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
settings.USE_TZ = False

django.setup()

if __name__ == '__main__':
    from tasks.models import Task, TaskCompletions
    Task.objects.all().delete()
    TaskCompletions.objects.all().delete()

    task = Task(
        title='Acordar cedo',
        desired_weekly_frequency=5
    )

    task_completion = TaskCompletions(
        task_id = task
    )

    task.save()
    task_completion.save()
