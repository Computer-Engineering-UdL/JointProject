from django.http import JsonResponse
from django.shortcuts import render
from Reception.forms import AddClientForm, RoomReservationForm, RoomForm, InfoClientForm
from Reception.models import Room, RoomReservation, Client


def worker_home(request):
    return render(request, 'worker/base_worker.html')


# Create your views here.
def add_client(request):
    """Add a new client to the database."""
    if request.method == 'POST':
        form = AddClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.username = 'default'
            client.save()
    else:
        form = AddClientForm()
    return render(request, 'worker/reception/add_client.html', {'form': form})


def room_reservation(request):
    """Reserve a room for a client."""
    if request.method == 'POST':
        form = RoomReservationForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print("Form is not valid. Errors: ", form.errors)
    else:
        form = RoomReservationForm()
    return render(request, 'worker/reception/room_reservation.html', {'form': form})


def add_room(request):
    """Add a new room to the database."""
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            chosen_room = form.cleaned_data['room']
            Room.objects.get(id=chosen_room.id)
            form.save()
    else:
        form = RoomForm()
    return render(request, 'worker/reception/add_room.html', {'form': form})


# Check-in views
def check_in_1(request):
    """Check-in a client."""
    if request.method == 'POST':
        form = InfoClientForm(request.POST)
        if form.is_valid():
            form.save()
            num_reservation = form.cleaned_data['num_reservation']
            dni = form.cleaned_data['dni']
            client = None
            reservation = None
            if num_reservation:
                try:
                    reservation = RoomReservation.objects.get(id=num_reservation)
                    # client = reservation.client
                except RoomReservation.DoesNotExist:
                    pass
            if dni and not client:
                try:
                    client = Client.objects.get(id_number=dni)
                    # reservation = RoomReservation.objects.get(client=client)
                except Client.DoesNotExist:
                    pass
            if client or reservation:
                return render(request, 'reception/check_in_2.html', {'client': client, 'reservation': reservation})
            else:
                form.add_error(None, "No existeix cap reserva amb aquestes dades.")
    else:
        form = InfoClientForm()
    return render(request, 'worker/reception/check_in_1.html', {'form': form})


def fetch_rooms(request):
    room_type = request.GET.get('room_type')
    rooms = Room.objects.filter(room_type=room_type, is_taken=False).order_by('room_num')
    data = {'rooms': list(rooms.values('id', 'room_num'))}
    return JsonResponse(data)


# Check in views

def check_in_2(request):
    return render(request, 'reception/check_in_2.html', {})
