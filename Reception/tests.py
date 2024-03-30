from django.test import TestCase
from django.urls import reverse
from Reception.models import RoomReservation, Client, Room


class CheckInViewTest(TestCase):

    def setUp(self):
        room = Room.objects.create(room_num=201, room_price=50, room_type='Double', is_clean=True, is_taken=False)
        self.reservation = RoomReservation.objects.create(id=5, room=room, entry='2021-01-01', exit='2021-01-02', num_guests=2)
        self.client_obj = Client.objects.create(id_number='12345678A', first_name='John', last_name='Doe', email='client@gmail.com', phone_number='123456789', is_hosted=False)

    def test_check_in_view_status_code(self):
        url = reverse('check_in')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_check_in_view_form_errors(self):
        url = reverse('check_in')
        response = self.client.post(url, {})
        self.assertContains(response, "Introdueix el número de reserva o el número del document identificatiu")


    def test_check_in_view_redirect_with_reservation(self):
        url = reverse('check_in')
        response = self.client.post(url, {'num_reservation': self.reservation.id})
        self.assertTemplateUsed(response, 'reception/check_in_2.html')

    def test_check_in_view_redirect_with_dni(self):
        url = reverse('check_in')
        response = self.client.post(url, {'dni': self.client_obj.id_number})
        self.assertTemplateUsed(response, 'reception/check_in_2.html')
