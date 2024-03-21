from django.shortcuts import render, redirect
from django.contrib import messages

from Reception.forms import AddClientForm, RoomReservationForm
from user.forms import SignUpForm


def signup(request):
    """Sign up a new user."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def add_client(request):
    """Add a new client to the database."""
    if request.method == 'POST':
        form = AddClientForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = AddClientForm()
    return render(request, 'add_client.html', {'form': form})


def room_reservation(request):
    """Reserve a room for a client."""
    if request.method == 'POST':
        form = RoomReservationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = RoomReservationForm()
    return render(request, 'room_reservation.html', {'form': form})
