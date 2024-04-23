from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Task
# Create your views here.
def all_tasks_view(request:HttpRequest):

    return render(request, 'tasks/all_tasks.html')