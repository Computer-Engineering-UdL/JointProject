from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from User.forms import SignUpForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from JointProject.settings import LOGOUT_REDIRECT_URL
from User.decorators import worker_required


def redirect_user_based_on_type(user):
    """Determines the URL depending on the type of User."""
    # Workers
    if hasattr(user, 'worker'):
        worker_type_to_url = {
            'worker': 'worker_home',
            'receptionist': 'receptionist_home',
        }
        return worker_type_to_url.get(user.worker.type, 'base')
    # Not workers
    else:
        return 'base'


def signup(request):
    """Sign up a new User."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the User after signing up
            messages.success(request, 'Account created successfully')
            return redirect(redirect_user_based_on_type(user))
        else:
            messages.error(request, 'Please correct the error below')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def login_custom(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(redirect_user_based_on_type(user))
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect(LOGOUT_REDIRECT_URL)


@worker_required('worker')
def worker_home(request):
    return render(request, 'worker/base_worker.html')


def home(request):
    return render(request, 'base.html')
