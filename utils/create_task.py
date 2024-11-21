import os
import sys
import django
from pathlib import Path
from django.conf import settings

from django.shortcuts import get_object_or_404

DJANGO_BASE_DIR = Path(__file__).parent.parent

sys.path.append(str(DJANGO_BASE_DIR))
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
settings.USE_TZ = False

django.setup()

if __name__ == '__main__':
    from tasks.models import Task, TaskCompletions
    # Task.objects.all().delete()
    # TaskCompletions.objects.all().delete()

    # task_title = ['Acordar cedo', 'Beber muita água', 'Ir pra academia']
    # task_frequency = [5, 7, 5]
    
    # for i in range(len(task_title)):
    #     task = Task(
    #         title=task_title[i],
    #         desired_weekly_frequency=task_frequency[i]
    #     )


    #     task.save()
    
    # task_completion = TaskCompletions(
    #     task_id = task
    # )
    # task_completion.save()

    # query = get_object_or_404(Task, title="Beber muita água")
    # task_completion = TaskCompletions(
    #     task_id = query 
    # )
    # task_completion.save()
    # TaskCompletions.objects.filter(id=58).delete()
    # Task.objects.filter(title="teste").delete()
