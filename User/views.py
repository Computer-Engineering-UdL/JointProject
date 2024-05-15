from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from User.forms import SignUpForm, PopulateForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from JointProject.settings import LOGOUT_REDIRECT_URL
from User.decorators import worker_required, admin_required
from db_populator import populate_functions, get_active_reservations_without_expenses
from Cleaner.config import MATERIALS_NAMES

worker_type_to_url = {
    'receptionist': 'receptionist_home',
    'cleaner': 'cleaner_home',
    'restaurant': 'restaurant_home',
    'accountant': 'accountant_home',
    'planner': 'planner_home'
}


def redirect_user_based_on_type(user):
    """Determines the URL depending on the type of User."""
    # Workers
    if hasattr(user, 'worker'):
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
            messages.success(request, "El compte s'ha creat correctament")
            return redirect(redirect_user_based_on_type(user))
        else:
            messages.error(request, "Error al crear el compte")
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
        messages.error(request, "Usuari o contrasenya incorrectes")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect(LOGOUT_REDIRECT_URL)


@login_required
def home(request):
    return render(request, 'base.html')


@admin_required
def populate(request):
    if request.method == 'POST':
        form = PopulateForm(request.POST)
        if form.is_valid():
            data_type = form.cleaned_data['data_type']
            entries = form.cleaned_data['entries']
            # Since stock and materials len must be the same as the MATERIALS_NAMES list, the entries must be changed
            if data_type == 'stock' or data_type == 'materials':
                entries = len(MATERIALS_NAMES)
            populate_function = populate_functions.get(data_type)

            if populate_function:
                if data_type == 'expenses':
                    entries = get_active_reservations_without_expenses().count()
                    populate_function()
                else:
                    populate_function(entries)
                if entries == 0:
                    messages.info(request, f"No entries were populated for {data_type}")
                elif entries == 1:
                    messages.success(request, f"Successfully populated {entries} entry for {data_type}")
                else:
                    messages.success(request, f"Successfully populated {entries} entries for {data_type}")
            else:
                messages.error(request, "No valid function found for the selected data type")

    else:
        form = PopulateForm()

    return render(request, 'admin-tests/populate.html', {'form': form})
