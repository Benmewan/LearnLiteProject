from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib import messages
from .models import UserProfileForm



def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')

        # Check if passwords match
        if password != repeat_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'accounts/register.html')  

        try:
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose a different one.")
                return render(request, 'accounts/register.html')

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email address is already in use. Please use a different one.")
                return render(request, 'accounts/register.html')
            
            # Create user
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            # Other user creation logic

            messages.success(request, "User registered successfully.")
            return render(request, 'accounts/login.html')  
        
        except IntegrityError:
            messages.error(request, "An error occurred during registration. Please try again.")
            return render(request, 'accounts/register.html')

    return render(request, 'accounts/register.html')


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

def Subscribe(request):
    return render(request, 'accounts/Subscribe.html')