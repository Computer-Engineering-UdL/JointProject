from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django import forms
from Reception.models import RoomReservation, Client, Room, Worker
from Reception.config import Config as c
from Reception.forms import SearchReservationForm


class BaseTest(TestCase):

    def setUp(self):
        self.worker = Worker.objects.create_user(
            username='john_worker',
            email='worker@example.com',
            password='testpassword123',
            type='cleaner'
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


class TestStatusCode(BaseTest):

    def test_cleaner_home_status_code(self):
        url = reverse('cleaner_home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_cleaner_stock_status_code(self):
        url = reverse('cleaner_stock')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_cleaner_cleaner_cleaned_rooms_status_code(self):
        url = reverse('cleaner_cleaned_rooms')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
