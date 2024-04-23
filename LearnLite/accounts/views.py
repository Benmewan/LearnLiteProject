from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError

def register_user(request):
#This Messgae will appear if user have some issues with sign up
    msg = None

    if request.method == 'POST':
        try:
            #create new user
            new_user = User.objects.create_user(
                username=request.POST["username"], 
                email=request.POST["email"], 
                first_name=request.POST["first_name"], 
                last_name=request.POST["last_name"], 
                password=request.POST["password"]
            )
            new_user.save()
            #redirect to login page
            return redirect("accounts:user_login")
        except IntegrityError as e:
            msg = "Username already exists. Please choose a different username."
            print(e)

        except Exception as e:
            msg = f"Something went wrong. Please try again... {e}"
            print(e)
    return render(request, 'accounts/register.html', {'msg':msg})

def user_login(request):
#the message will appear if the user enter wrong data
    msg = None

    if request.method == 'POST':

        #Authenticate the user by username and password
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        #this is means if user exist    
        if user:
            login(request, user)
            return redirect('main:index_view')
        else:
            msg = "Username or Password is wrong, Please try Again!!"

    return render(request, 'accounts/login.html', {'msg':msg})

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('accounts/login.html')  