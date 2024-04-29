from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django import forms
from Reception.models import RoomReservation, Client, Room, Worker
from Cleaner.models import Stock, CleaningMaterial, CleanedRoom
from Cleaner.config import Config as c
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

        self.cleaning_material_esponja = CleaningMaterial.objects.create(
            material_name='Esponja',
            image='esponja.png'
        )
        self.cleaning_material_spray = CleaningMaterial.objects.create(
            material_name='Spray',
            image='spray.png'
        )

        self.client.force_login(self.worker)


class TestStatusCode(BaseTest):

    def test_cleaner_home_status_code(self):
        url = reverse('cleaner_home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_cleaner_stock_status_code(self):
        url = reverse('cleaner_stock')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_cleaner_cleaner_cleaned_rooms_status_code(self):
        url = reverse('cleaner_cleaned_rooms')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_cleaner_cleaner_cleaned_room_info_status_code(self):
        url = reverse('cleaner_cleaned_room_info', args=[self.room.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

class TestCleanerRedirects(BaseTest):

    def test_cleaner_stock_esponja(self):
        url = reverse('cleaner_stock')
        response = self.client.post(url, {'material_name': self.cleaning_material_esponja.material_name})
        self.assertTemplateUsed(response, c.get_cleaner_stock_path(1))

    def test_cleaner_stock_spray(self):
        url = reverse('cleaner_stock')
        response = self.client.post(url, {'material_name': self.cleaning_material_spray.material_name})
        self.assertTemplateUsed(response, c.get_cleaner_stock_path(1))

    def test_cleaner_stock_all(self):
        url = reverse('cleaner_stock')
        response = self.client.post(url, {'material_name': ''})
        self.assertTemplateUsed(response, c.get_cleaner_stock_path(1))





