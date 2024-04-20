from django.shortcuts import render, redirect
from Cleaner.forms import StockForm, CleanedRoomForm
from Cleaner.models import Stock
from Reception.models import Room
from User.decorators import worker_required
from Cleaner.config import Config as c


@worker_required('cleaner')
def cleaner_home(request):
    return render(request, 'worker/cleaner/cleaner_home.html')


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
                stock_ids = request.POST.getlist('stock[]')
                for stock_id in stock_ids:
                    item = Stock.objects.get(id=stock_id)
                    item.is_available = not item.is_available
                    item.save()
                return redirect('cleaner_stock')
        else:
            stock = Stock.objects.filter(is_active=True)
    else:
        stock = Stock.objects.filter(is_active=True)

    return render(request, c.get_cleaner_stock_path(1), {'form': form, 'stock': stock})


@worker_required('cleaner')
def cleaner_cleaned_rooms(request):
    occupied_rooms = Room.objects.filter(is_taken=True, roomreservation__check_out_active=False)
    check_out_rooms = Room.objects.filter(is_taken=True, roomreservation__check_out_active=True)
    return render(request, c.get_cleaner_rooms_path(1), {'occupied_rooms': occupied_rooms,
                                                         'check_out_rooms': check_out_rooms})


@worker_required('cleaner')
def cleaner_cleaned_room_info(request, room_id):
    form = CleanedRoomForm(request.POST or None)
    room = Room.objects.get(id=room_id)

    if request.method == 'POST':
        if form.is_valid():
            missing_objects = form.cleaned_data.get('missing_objects')
            need_towels = form.cleaned_data.get('need_towels')
            additional_comments = form.cleaned_data.get('additional_comments')
            cleaned_room = room.cleanedroom_set.create(missing_objects=missing_objects,
                                                       need_towels=need_towels,
                                                       additional_comments=additional_comments,
                                                       is_cleaned=True)
            cleaned_room.save()
            return redirect('cleaner_cleaned_rooms')
    return render(request, c.get_cleaner_rooms_path(2), {'room': room})
