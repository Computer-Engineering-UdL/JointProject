from django.shortcuts import render, redirect
from django.contrib import messages
from Planner.forms import RoomForm, CreateWorker
from Reception.models import Worker
from Planner.config import Config as c
from User.forms import SignUpForm
from User.decorators import worker_required
from User.config import Config as uc


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

    return render(request, c.get_add_room_path(), {'form': form})


@worker_required('planner')
def planner_home(request):
    """Render the planner home page."""
    return render(request, c.get_planner_home_path())


@worker_required('planner')
def room_assignment(request):
    """Assign a room to a client."""

    return render(request, c.get_room_assignment_path())


@worker_required('planner')
def new_worker(request):
    """Register a new worker."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        create_worker_form = CreateWorker(request.POST)
        if form.is_valid() and create_worker_form.is_valid():
            user = form.save()
            user_type = create_worker_form.cleaned_data.get('worker_type')

            if user_type in uc.get_worker_type_to_url():
                worker = Worker(hoteluser_ptr_id=user.pk, type=user_type)
                worker.save_base(raw=True)
                user.worker = worker
                user.save()

            messages.success(request, "Treballador afegit amb èxit")
            return redirect('planner_home')
        else:
            messages.error(request, "Error al afegir el treballador")
    else:
        form = SignUpForm()
        create_worker_form = CreateWorker()

    return render(request, c.get_new_worker_path(), {'form': form, 'create_worker_form': create_worker_form})
