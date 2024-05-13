from django.shortcuts import render, get_object_or_404, redirect

from Reception.forms import RoomReservationForm
from Reception.models import RoomReservation, create_despesa, Room, Client
from Reception.config import Config as c


# Create your views here.
def guest_reservation_1(request):
    """Client creates a new reservation."""
    if request.method == 'POST':
        form = RoomReservationForm(request.POST)
        if form.is_valid():
            room_rsv = form.save(commit=False)
            room = Room.objects.get(room_type=room_rsv.room.room_type, is_taken=False)
            client = Client.objects.get(id=request.user.id)
            room.is_taken = True
            room_rsv.save()
            room.save()
            room_reservation = get_object_or_404(RoomReservation, pk=room_rsv.id)
            create_despesa(room_rsv, room_reservation.pension_type, room.room_type)
            return redirect('base_guest.html')
    else:
        form = RoomReservationForm()

    return render(request, c.get_reservation_path(1), {'form': form})
