from django.shortcuts import render, redirect
from django.contrib import messages
from Planner.forms import RoomForm
from Reception.config import Config as c
from User.decorators import worker_required


@worker_required('planner')
def add_room(request):
    """Add a new room to the database."""
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Habitació afegida amb èxit")
            return redirect('planner_home')
    else:
        form = RoomForm()

    return render(request, c.get_admin_tests_path(2), {'form': form})


@worker_required('planner')
def planner_home(request):
    """Render the planner home page."""
    return render(request, c.get_admin_tests_path(1))
