from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from Reception.models import RoomReservation, Client, Room, Worker
from Reception.config import Config as c


class CheckInViewTest(TestCase):

    def setUp(self):
        self.worker = Worker.objects.create_user(
            username='john_worker',
            email='worker@example.com',
            password='testpassword123',
            type='receptionist'
        )

        self.client_user = Client.objects.create_user(
            username='john_doe',
            email='client@example.com',
            password='clientpassword',
            id_number='12345678A',
            first_name='John',
            last_name='Doe',
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
            client=self.client_user,
            room=self.room,
            entry=timezone.now().date(),
            exit=(timezone.now() + timezone.timedelta(days=1)).date(),
            pension_type='Sense pensió',
            num_guests=2
        )
        self.client.force_login(self.worker)

    def test_check_in_view_status_code(self):
        url = reverse('check_in')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_room_reservation(self):
        url = reverse('new_reservation_1')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_check_out(self):
        url = reverse('check_out')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
