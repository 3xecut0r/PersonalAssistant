from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm

from Utils.views import create_dropbox_folders


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'Users/password_reset.html'
    email_template_name = 'Users/password_reset_email.html'
    html_email_template_name = 'Users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'Users/password_reset_subject.txt'


def main_page(request):
    return render(request, 'Users/main_page.html')


def signupuser(request):
    if request.user.is_authenticated:
        return redirect(to='contacts:start_page')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            user = User.objects.get(username=username)
            create_dropbox_folders(request, user_id=user.id)
            return redirect(to='users:login')
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
    return redirect(to='users:main_page')
