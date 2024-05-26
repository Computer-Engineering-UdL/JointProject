from datetime import datetime

from Reception.models import HotelUser, Client
from Restaurant.models import RestaurantReservation


def get_client_type(id_number):
    try:
        user = HotelUser.objects.get(id_number=id_number)
        client = Client.objects.get(hoteluser_ptr_id=user.id)
    except HotelUser.DoesNotExist:
        return 'external'

    if client.is_hosted:
        return 'internal'
    return 'external'


def create_restaurant_reservation(reservation_data):
    RestaurantReservation.objects.create(
        day=datetime.strptime(reservation_data['day'], '%Y-%m-%d').date(),
        num_guests=reservation_data['num_guests'],
        service=reservation_data['service'],
        is_active=True,
        client_id=get_client_id(reservation_data['id_number'])
    )


def get_client_id(id_number):
    try:
        user = HotelUser.objects.get(id_number=id_number)
        client = Client.objects.get(hoteluser_ptr_id=user.id)
    except HotelUser.DoesNotExist:
        return None

    return client.id
