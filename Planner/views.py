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

    return render(request, 'worker/planner/add_room.html', {'form': form})


@worker_required('planner')
def planner_home(request):
    """Render the planner home page."""
    return render(request, 'worker/planner/planner_home.html')


@worker_required('planner')
def room_assignment(request):
    """Assign a room to a client."""
    return render(request, 'worker/planner/room_assignment.html')


@worker_required('planner')
def new_worker(request):
    """Register a new worker."""
    return render(request, 'worker/planner/new_worker.html')
