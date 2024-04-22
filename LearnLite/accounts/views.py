from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
def register_view(request:HttpRequest):
    return render(request, 'accounts/register.html')
