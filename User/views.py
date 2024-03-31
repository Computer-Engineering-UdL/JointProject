from django.shortcuts import render, redirect
from django.contrib import messages
from User.forms import SignUpForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


def signup(request):
    """Sign up a new User."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the User after signing up
            messages.success(request, 'Account created successfully!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')
    # return render(request, 'registration/logged_out.html', {})
