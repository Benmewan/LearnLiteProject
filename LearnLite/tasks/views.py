from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Task
# Create your views here.
def all_tasks_view(request:HttpRequest):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'tasks/all_tasks.html', {'tasks':tasks})

def add_task_view(request:HttpRequest):
    if request.method == 'POST':
        try:
            new_task = Task(
                user = request.user,
                title = request.POST['title'],
                description = request.POST['description'],
                due_date = request.POST['due_date'],
                is_done = request.POST.get('is_done', False)
            )
            new_task.save()
            return redirect('tasks:all_tasks_view')
        except Exception as e:
            print(e)
    return render(request, 'tasks/add_task.html')

def update_task_status_view(request:HttpRequest, task_id):
    try:
        # Attempt to get the task
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return render(request, "main/not_exist.html")
    try:
        task.is_done = True
        task.save()
    except Exception as e:
        # Handle other exceptions
        print(e)

    return redirect("tasks:all_tasks_view")