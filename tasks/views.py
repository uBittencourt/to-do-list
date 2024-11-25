from datetime import date
from django.db.models import Count
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, redirect, get_object_or_404

from tasks.forms import TaskForm 
from tasks.models import Task, TaskCompletions
from utils.get_date import get_last_day_of_week, get_first_day_of_week


def index(request):
    first_day_of_week = get_first_day_of_week(date.today())
    last_day_of_week = get_last_day_of_week(date.today())

    _pending_tasks = pending_tasks(first_day_of_week, last_day_of_week) 
    summary = summary_of_week(first_day_of_week, last_day_of_week)

    count_pending, count_completed = 0, 0
    for task in _pending_tasks:
        count_pending += task['desired_weekly_frequency']
        count_completed += task['completion_count']
    
    try:
        count_completed_percent = (count_completed * 100) // count_pending
    except:
        count_completed_percent = 0

    if request.method == 'POST':
        if request.POST.get('task'):
            task_sent = request.POST.get('task')
            task = get_object_or_404(Task, id=task_sent)
            task_completion = TaskCompletions(
                task_id = task    
            )
            task_completion.save()
            return redirect('tasks:index')
        elif request.POST.get('id_completion'):
            id_completion = int(request.POST.get('id_completion'))
            TaskCompletions.objects.filter(id=id_completion).delete()
            return redirect('tasks:index')
        else:
            print('entrou aqui poha')
            return redirect('tasks:previous_week')

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
            'tasks/index.html',
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


def pending_tasks(first_day, last_day):
    tasks_created_up_to_week = Task.objects\
        .values("id", "title", "desired_weekly_frequency")\
        .filter(created_at__range=(first_day, last_day))
    
    task_completion_count = TaskCompletions.objects\
        .values("task_id")\
        .annotate(completion_count=Count("task_id"))\
        .filter(created_at__range=(first_day, last_day))
    
    for task in tasks_created_up_to_week:
        for completion in task_completion_count:
            if task['id'] == completion['task_id']:
                task['completion_count'] = completion['completion_count']
    
    for task in tasks_created_up_to_week:
        if not 'completion_count' in task:
            task['completion_count'] = 0
    
    return tasks_created_up_to_week


def summary_of_week(first_day, last_day):
    tasks_created_up_to_week = Task.objects\
        .values("id", "title", "desired_weekly_frequency")\
        .filter(created_at__range=(first_day, last_day))
    
    tasks_completed = TaskCompletions.objects\
        .values("task_id", "created_at", "id")\
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
                    .append([task['title'], completion['completion_time'], completion['id']])

    return summary


def previous_week(request):
    first_day_of_week = get_first_day_of_week(date.today() - relativedelta(days=7))
    last_day_of_week = get_last_day_of_week(first_day_of_week)

    _pending_tasks = pending_tasks(first_day_of_week, last_day_of_week) 
    summary = summary_of_week(first_day_of_week, last_day_of_week)

    count_pending, count_completed = 0, 0
    for task in _pending_tasks:
        count_pending += task['desired_weekly_frequency']
        count_completed += task['completion_count']
    
    count_completed_percent = (count_completed * 100) // count_pending

    if request.method == 'POST':
        return redirect('tasks:index')

    return render(
        request,
        'tasks/previous_week.html',
        {
            'first_day': f'{first_day_of_week.strftime('%d/%m/%Y')}',
            'last_day': f'{last_day_of_week.strftime('%d/%m/%Y')}',
            'summary': summary,
            'count_completed_percent': count_completed_percent,
            'count_completed': count_completed,
            'count_pending': count_pending
        }    
    )
