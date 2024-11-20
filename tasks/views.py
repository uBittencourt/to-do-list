from datetime import date
from django_cte import With
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.db.models import Count
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, redirect, get_object_or_404

from tasks.forms import TaskForm 
from tasks.models import Task, TaskCompletions
from utils.get_date import get_last_day_of_week, get_first_day_of_week

# Create your views here.
def index(request):
    first_day_of_week = get_first_day_of_week(date.today())
    last_day_of_week = get_last_day_of_week(date.today())

    _pending_tasks = pending_tasks() 
    summary = summary_of_week()

    count_pending, count_completed = 0, 0
    for task in pending_tasks():
        count_pending += task['desired_weekly_frequency']
        count_completed += task['completion_count']
    
    count_completed_percent = (count_completed * 100) // count_pending

    if request.method == 'POST':
        task_sent = request.POST.get('task')
        task = get_object_or_404(Task, id=task_sent)
        task_completion = TaskCompletions(
            task_id = task    
        )
        task_completion.save()
        return redirect('tasks:index')

    print(summary)
    return render(
        request,
        'tasks/index.html',
        {
            'first_day': f'{first_day_of_week.strftime('%d/%m/%Y')}',
            'last_day': f'{last_day_of_week.strftime('%d/%m/%Y')}', 
            'pending_tasks': _pending_tasks,
            'summary': summary,
            'count_completed_percent': count_completed_percent,
            'count_completed': count_completed,
            'count_pending': count_pending
        }
    )


def create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        context = {
            'form': form    
        }
    
        if form.is_valid():
            form.save()
            return redirect('tasks:index')
    
        return render(
            request,
            'tasks/create_task.html',
            context    
        )
    
    context = {
        'form': TaskForm(),    
    }

    return render(
        request, 
        'tasks/create_task.html',
        context
    )


def pending_tasks():
    first_day = get_first_day_of_week(date.today())
    last_day = get_last_day_of_week(date.today())

    tasks_created_up_to_week = Task.objects\
        .values("id", "title", "desired_weekly_frequency")\
        .filter(created_at__range=(first_day, last_day))
    
    task_completion_count = TaskCompletions.objects\
        .values("task_id")\
        .annotate(completion_count=Count("task_id"))\
        .filter(created_at__range=(first_day, last_day))
    
    # ADICIONAR TUDO AGORA NO MESMO DICIONARIO, VALIDANDO DE O ID DA TESK É IGUAL O TASK_ID DA COMPLETIONS
    # SE DER CERTO AJEITAR CÓDIGO QUE ESTÁ UMA MERDA
    # print()
    # print(tasks_created_up_to_week)
    # print(task_completion_count)
    # print()
    for task in tasks_created_up_to_week:
        for completion in task_completion_count:
            if task['id'] == completion['task_id']:
                task['completion_count'] = completion['completion_count']
    
    for task in tasks_created_up_to_week:
        if not 'completion_count' in task:
            task['completion_count'] = 0
    
    # for task in tasks_created_up_to_week:
    #     print(task)

    return tasks_created_up_to_week

    # return render(
    #     request,
    #     'tasks/index.html'    
    # )


def summary_of_week():
    first_day = get_first_day_of_week(date.today())
    last_day = get_last_day_of_week(date.today())

    tasks_created_up_to_week = Task.objects\
        .values("id", "title", "desired_weekly_frequency")\
        .filter(created_at__range=(first_day, last_day))
    
    tasks_completed = TaskCompletions.objects\
        .values("task_id", "created_at")\
        .filter(created_at__range=(first_day, last_day))
    
    for task in tasks_completed:
        task['completion_date'] = task['created_at'] - relativedelta(hours=3)
        task['completion_date'] = task['completion_date'].strftime('%d/%m/%Y')
        task['completion_time'] = task['created_at'] - relativedelta(hours=3)
        task['completion_time'] = task['completion_time'].strftime('%Hh%Mmin')

    summary = dict()
    for task in tasks_created_up_to_week:
        for completion in tasks_completed:
            if not completion['completion_date'] in summary:
                summary[f'{completion['completion_date']}'] = []

            if task['id'] == completion['task_id'] and \
                task['title'] not in summary[f'{completion['completion_date']}']:
                summary[f'{completion['completion_date']}']\
                    .append([task['title'], completion['completion_time']])

    return summary
    
# TESTS 
# from itertools import chain
# print(list(chain(tasks_created_up_to_week, task_completion_count)))
# pending_tasks = Task.objects.values('title', 'desired_weekly_frequency')\
#     .with_cte(tasks_created_up_to_week)\
    # .select_related(task_completion_count+)
    
# test = tasks_created_up_to_week.union(task_completion_count)
# pending_tasks_2 = TaskCompletions.objects.values('task_id', 'completionCount')\
#     .with_cte(task_completion_count)