
from Reception.models import HotelUser, Client

def get_client_type(id_number):
    user = HotelUser.objects.get(id_number=id_number)
    client = Client.objects.get(hoteluser_ptr_id=user.id)

    if user and client.is_hosted:
        return 'internal'
    return 'external'

