from django.shortcuts import render,redirect
from django.http import Http404
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from todo.models import Task


def index(request):

    if request.method == 'POST':
        task = Task(title=request.POST['title'],
                    due_at=make_aware(parse_datetime(request.POST['due_at'])))
        task.save()

    if request.GET.get('order') == 'due':
        tasks = Task.objects.order_by('due_at')
    else:
        tasks = Task.objects.order_by('-posted_at')

    tasks = Task.objects.all()

    if request.GET.get('order') == 'due':
        tasks_query = Task.objects.order_by('due_at')
    else:
        tasks_query = Task.objects.order_by('-posted_at')

    query = request.GET.get('q')
    if query:
        tasks = tasks_query.filter(title__icontains=query)
    else:
        tasks = tasks_query

    context = {
        'tasks': tasks,
        'query': query,
    }
    return render(request, 'todo/index.html', context)

def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404('Task does not exist')
    
    context = {
        'task': task,
    }
    return render(request, 'todo/detail.html', context)

def update(request, task_id):
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            raise Http404('Task does not exist')

        if request.method == 'POST':
            task.title = request.POST['title']
            task.due_at = make_aware(parse_datetime(request.POST['due_at']))
            task.save()
            return redirect(detail,task_id) # トップページ（一覧画面）に自動で戻る
            
        # 普通にページを開いたとき（編集画面の表示）
        context = {
            'task': task
        }
        return render(request, 'todo/edit.html', context)
def delete(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404('Task does not exist')

    task.delete()
    return render(request, 'todo/delete.html')
