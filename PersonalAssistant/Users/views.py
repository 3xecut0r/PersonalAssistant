from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm

from Utils.views import create_user_folders
from Utils.models import UserFiles

def signupuser(request):
    if request.user.is_authenticated:
        return redirect(to='contacts:start_page')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            user = User.objects.get(username=username)
            create_user_folders(user_id=user.id)
            user_files = UserFiles(user_id=user.id)
            user_files.save()
            return redirect(to='contacts:start_page')
        else:
            return render(request, 'Users/signup.html', context={"form": form})

    return render(request, 'Users/signup.html', context={"form": RegisterForm()})


def loginuser(request):
    if request.user.is_authenticated:
        return redirect(to='contacts:start_page')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Username or password didn\'t match')
            return redirect(to='users:login')

        login(request, user)
        return redirect(to='contacts:start_page')

    return render(request, 'Users/login.html', context={"form": LoginForm()})

@login_required
def logoutuser(request):
    logout(request)
    return redirect(to='contacts:start_page')
