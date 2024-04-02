from django.shortcuts import render, redirect
from django.contrib import messages
from User.forms import SignUpForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from JointProject.settings import LOGOUT_REDIRECT_URL
from User.decorators import worker_required


def signup(request):
    """Sign up a new User."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the User after signing up
            messages.success(request, 'Account created successfully!')
            return redirect('base')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect(LOGOUT_REDIRECT_URL)


@worker_required('worker')
def worker_home(request):
    return render(request, 'worker/base_worker.html')


def home(request):
    return render(request, 'base.html')
