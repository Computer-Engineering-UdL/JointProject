from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from Reception.models import RoomReservation, Client, Room


class CheckInViewTest(TestCase):

    def setUp(self):
        self.client_obj = Client.objects.create(
            username='john_doe',
            id_number='12345678A',
            first_name='John',
            last_name='Doe',
            email='client@gmail.com',
            phone_number='123456789',
            is_hosted=False
        )

        self.room = Room.objects.create(
            is_clean=True,
            is_taken=False,
            room_num=201,
            room_price=50,
            room_type='Double'
        )

        self.reservation = RoomReservation.objects.create(
            client=self.client_obj,
            room=self.room,
            entry=timezone.now().date(),
            exit=(timezone.now() + timezone.timedelta(days=1)).date(),
            num_guests=2
        )

    def test_check_in_view_status_code(self):
        url = reverse('check_in')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_check_in_view_redirect_with_reservation(self):
        url = reverse('check_in')
        response = self.client.post(url, {'num_reservation': self.reservation.id})
        self.assertTemplateUsed(response, 'worker/receptionist/check-in/check_in_2.html')

    def test_check_in_view_redirect_with_dni(self):
        url = reverse('check_in')
        response = self.client.post(url, {'dni': self.client_obj.id_number})
        self.assertTemplateUsed(response, 'worker/receptionist/check-in/check_in_2.html')
