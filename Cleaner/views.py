from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from Cleaner.forms import StockForm, CleanedRoomForm
from Cleaner.models import Stock, CleanedRoom
from Reception.models import Room
from User.decorators import worker_required
from Cleaner.config import Config as c


@worker_required('cleaner')
def cleaner_home(request):
    return render(request, c.get_cleaner_home_path(1))


@worker_required('cleaner')
def cleaner_stock(request):
    form = StockForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            material_name = form.cleaned_data.get('material')
            if material_name:
                stock = Stock.objects.filter(material__material_name__icontains=material_name, is_active=True)
            else:
                stock = Stock.objects.filter(is_active=True)

            if 'update_stock' in request.POST:
                submitted_stock_ids = set(map(int, request.POST.getlist('stock[]')))
                all_active_stocks = set(Stock.objects.filter(is_active=True).values_list('id', flat=True))

                for stock_id in all_active_stocks:
                    item = Stock.objects.get(id=stock_id)
                    item.is_available = stock_id not in submitted_stock_ids
                    item.save()
                messages.success(request, 'Stock actualitzat correctament')

                return redirect('cleaner_stock')
        else:
            stock = Stock.objects.filter(is_active=True)
    else:
        stock = Stock.objects.filter(is_active=True)

    return render(request, c.get_cleaner_stock_path(1), {'form': form, 'stock': stock})


@worker_required('cleaner')
def cleaner_cleaned_rooms(request):
    today = timezone.now().date()

    occupied_rooms = Room.objects.filter(
        is_taken=True,
        roomreservation__exit__gt=today,
        roomreservation__check_out_active=False
    ).distinct()

    check_out_rooms = Room.objects.filter(
        is_taken=False,
        roomreservation__exit__gte=today,
        roomreservation__check_out_active=True
    ).distinct()

    return render(request, c.get_cleaner_rooms_path(1), {
        'occupied_rooms': occupied_rooms,
        'check_out_rooms': check_out_rooms
    })


@worker_required('cleaner')
def cleaner_cleaned_room_info(request, room_id):
    room = Room.objects.get(id=room_id)
    cleaned_rooms = CleanedRoom.objects.filter(room=room)
    initial_data = {
        'missing_objects': cleaned_rooms.first().missing_objects if cleaned_rooms.exists() else '',
        'need_towels': cleaned_rooms.first().need_towels if cleaned_rooms.exists() else 0,
        'additional_comments': cleaned_rooms.first().additional_comments if cleaned_rooms.exists() else ''
    }

    if request.method == 'POST':
        form = CleanedRoomForm(request.POST)
        if form.is_valid():
            if cleaned_rooms.exists():
                cleaned_room = cleaned_rooms.first()
                cleaned_room.missing_objects = form.cleaned_data.get('missing_objects')
                cleaned_room.need_towels = form.cleaned_data.get('need_towels')
                cleaned_room.additional_comments = form.cleaned_data.get('additional_comments')
                cleaned_room.save()
            else:
                missing_objects = form.cleaned_data.get('missing_objects')
                need_towels = form.cleaned_data.get('need_towels')
                additional_comments = form.cleaned_data.get('additional_comments')
                cleaned_room = CleanedRoom(
                    room=room,
                    missing_objects=missing_objects,
                    need_towels=need_towels,
                    additional_comments=additional_comments
                )
                cleaned_room.save()

            room.is_clean = True
            room.save()
            messages.success(request, 'Habitació actualitzada correctament')
        return redirect('cleaner_home')
    else:
        form = CleanedRoomForm(initial=initial_data)
    return render(request, c.get_cleaner_rooms_path(2), {'form': form, 'room': room})
