from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib import messages
from .models import UserProfileForm



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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:index_view')  # Redirect to the home page upon successful login
        else:
            messages.error(request, "Incorrect username or password. Please try again.")

    return render(request, 'accounts/login.html')



def profile(request):
    return render(request, 'accounts/profile.html')

def profile_settings(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')  # Redirect to the same page after successful submission
        else:
            messages.error(request, 'Failed to update profile. Please correct the errors.')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/settings.html', {'form': form})  # Corrected template name


def user_logout(request):
    logout(request)
    messages.info(request, 'Your session has ended.')
    return redirect('accounts:user_login')