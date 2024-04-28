from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Task
from django.utils import timezone
from datetime import timedelta
import datetime
# Create your views here.
def all_tasks_view(request:HttpRequest):
    # Fetch all tasks by default
    tasks = Task.objects.all()

    # Get the search query from the request
    search_query = request.GET.get('search_query')

    # Filter tasks by search query if it exists
    if search_query:
        tasks = tasks.filter(title__icontains=search_query) | tasks.filter(description__icontains=search_query)

    # Get the selected radio button value from the request
    filter_option = request.GET.get('btnradio')

    # Filter tasks based on the selected radio button
    if filter_option == 'btnradio2':  # Almost Due
        now = timezone.now()
        almost_due_date = now + timedelta(days=3)
        tasks = tasks.filter(due_date__lte=almost_due_date, is_done=False)
        tasks = tasks.filter(due_date__lte=almost_due_date)  # Filter tasks due within the calculated range
    elif filter_option == 'btnradio3':  # Newest
        tasks = tasks.order_by('-created_at')  # Order tasks by newest first
    elif filter_option == 'btnradio4':  # Finished
        tasks = tasks.filter(is_done=True)  # Filter tasks that are finished
    
    current_datetime = timezone.now()
    for task in tasks:
        time_difference = task.due_date - current_datetime
        if time_difference.total_seconds() > 0:
            if time_difference <= timedelta(hours=1):
                task.days_remaining = f"{int(time_difference.total_seconds() // 60)} minutes"
            elif time_difference <= timedelta(hours=24):
                hours_remaining = time_difference.total_seconds() // 3600
                minutes_remaining = (time_difference.total_seconds() % 3600) // 60
                task.days_remaining = f"{int(hours_remaining)} hours and {int(minutes_remaining)} minutes left"
            else:
                task.days_remaining = f"{int(time_difference.days)} days left"
            task.days_remaining_status = "future"
        else:
            minutes_passed = abs(time_difference.total_seconds()) // 60
            if minutes_passed < 60:
                task.days_remaining = f"{int(minutes_passed)} minutes ago"
            else:
                hours_passed = minutes_passed // 60
                if hours_passed < 24:
                    task.days_remaining = f"{int(hours_passed)} hours ago"
                else:
                    days_passed = hours_passed // 24
                    task.days_remaining = f"{int(days_passed)} days ago"
            task.days_remaining_status = "past"
    return render(request, 'tasks/all_tasks.html', {'tasks': tasks})

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

def update_task_status_to_true_view(request:HttpRequest, task_id):
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

def update_task_status_to_false_view(request:HttpRequest, task_id):
    try:
        # Attempt to get the task
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return render(request, "main/not_exist.html")

    try:
        task.is_done = False  # Set task status to False
        task.save()  # Save the task
    except Exception as e:
        # Handle other exceptions, such as database errors
        print(e)  # Print the error for debugging purposes

    return redirect("tasks:all_tasks_view")

def edit_task_view(request:HttpRequest, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return render(request, "main/not_exist.html")
    if request.method == 'POST':
        try:
            task.title = request.POST['title']
            task.description = request.POST['description']
            task.due_date = request.POST['due_date']
            task.is_done = request.POST.get('is_done', False) == 'on'
            task.save()
            return redirect('tasks:all_tasks_view')
        except Exception as e:
            print(e)
    return render(request, 'tasks/edit_task.html', {'task':task})

def delete_task_view(request:HttpRequest, task_id):
    try:
        task = Task.objects.get(pk=task_id)
        task.delete()
    except Task.DoesNotExist:
        return render(request, "main/not_exist.html")
    except Exception as e:
        print(e)
    return redirect("tasks:all_tasks_view")