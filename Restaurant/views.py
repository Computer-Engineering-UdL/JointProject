from django.shortcuts import render, redirect
from django.http import HttpResponse
from User.decorators import worker_required
from Restaurant.config import Config as c
from Restaurant.forms import NewRestaurantReservationForm
from Restaurant.models import RestaurantReservation


@worker_required('restaurant')
def restaurant_home(request):
    return render(request, c.get_restaurant_home_path(1))


@worker_required('restaurant')
def new_restaurant_reservation_1(request):
    if request.method == 'POST':
        form = NewRestaurantReservationForm(request.POST)
        if form.is_valid():
            request.session['reservation_data'] = request.POST
            return redirect('new_restaurant_reservation_2')
    else:
        form = NewRestaurantReservationForm()

    return render(request, c.get_restaurant_new_reservation_path(1), {'form': form})


@worker_required('restaurant')
def new_restaurant_reservation_2(request):
    reservation_data = request.session.get('reservation_data')
    if not reservation_data:
        return redirect('new_restaurant_reservation_1')

    if request.method == 'POST':
        form = NewRestaurantReservationForm(reservation_data)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.client = form.cleaned_data['client']
            reservation.save()
            del request.session['reservation_data']
            return redirect('restaurant_home')
        else:
            return render(request, c.get_restaurant_new_reservation_path(2), {'form': form})
    else:
        form = NewRestaurantReservationForm(initial=reservation_data)
        return render(request, c.get_restaurant_new_reservation_path(2), {'form': form})


@worker_required('restaurant')
def restaurant_reservations(request):
    reservations = RestaurantReservation.objects.filter(is_active=True)
    return render(request, c.get_restaurant_check_reservations_path(1), {'reservations': reservations})
