from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from datetime import date, timedelta
from .models import Contact
# Create your views here.

def index_view(request:HttpRequest):

    return render(request, "main/index.html")

def contact_view(request:HttpRequest):
    if request.method == "POST":
            new_message = Contact(name=request.POST["name"], 
                                  email=request.POST["email"],  
                                  message= request.POST["message"],)
            
            new_message.save()
    return render(request, "main/contact.html")

def about_view(request:HttpRequest):

    return render(request, "main/about.html")

def message_view(request:HttpRequest):
    if not request.user.is_superuser:
        # Render index template for non-staff users
        return render(request, "main/index.html")

    messages = Contact.objects.all()
    
    return render(request, "main/message.html", {"messages" : messages})