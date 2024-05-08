from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django import forms
from Reception.models import RoomReservation, Client, Room, Worker
from Cleaner.models import Stock, CleaningMaterial, CleanedRoom
from Cleaner.config import Config as c
from Cleaner.forms import StockForm, CleanedRoomForm
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
            is_clean=False,
            is_taken=False,
            room_num=201,
            room_price=50,
            room_type='Double'
        )
        self.room1 = Room.objects.create(
            is_clean=False,
            is_taken=False,
            room_num=202,
            room_price=50,
            room_type='Double'
        )

        self.room2 = Room.objects.create(
            is_clean=False,
            is_taken=True,
            room_num=203,
            room_price=50,
            room_type='Double'
        )

        self.reservation = RoomReservation.objects.create(
            client=self.client_user,
            room=self.room,
            entry=timezone.now().date(),
            exit=(timezone.now() + timezone.timedelta(days=1)).date(),
            pension_type='Sense pensió',
            num_guests=2,
            check_in_active=True
        )

        self.reservation1 = RoomReservation.objects.create(
            client=self.client_user,
            room=self.room1,
            entry=timezone.now().date(),
            exit=(timezone.now() + timezone.timedelta(days=2)).date(),
            pension_type='Sense pensió',
            num_guests=2,
            check_in_active=True
        )
        self.reservation2 = RoomReservation.objects.create(
            client=self.client_user,
            room=self.room2,
            entry=timezone.now().date(),
            exit=(timezone.now() + timezone.timedelta(days=2)).date(),
            pension_type='Sense pensió',
            num_guests=2,
            check_in_active=False,
            check_out_active=True
        )

        self.cleaning_material_esponja = CleaningMaterial.objects.create(
            material_name='Esponja',
            image='esponja.png'
        )
        self.cleaning_material_spray = CleaningMaterial.objects.create(
            material_name='Spray',
            image='spray.avif'
        )

        self.stock_esponja = Stock.objects.create(
            material=self.cleaning_material_esponja,
            price=1,
            is_available=True,
            is_active=True
        )
        self.stock_spray = Stock.objects.create(
            material=self.cleaning_material_spray,
            price=1,
            is_available=True,
            is_active=True
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

    def test_cleaner_stock_update(self):
        url = reverse('cleaner_stock')
        response = self.client.post(url, {'update_stock': 'update_stock'})
        self.assertRedirects(response, reverse('cleaner_stock'))

    def test_cleaned_room_info(self):
        url = reverse('cleaner_cleaned_room_info', args=[self.room.id])
        response = self.client.post(url, {'missing_objects': 'missing_objects',
                                          'need_towels': 2,
                                          'additional_comments': 'additional_comments'})
        self.assertRedirects(response, reverse('cleaner_home'))


class TestCleanerForms(BaseTest):

    def test_cleaner_stock_form_esponja(self):
        form = StockForm(data={'material': self.cleaning_material_esponja})
        self.assertTrue(form.is_valid())

    def test_cleaner_stock_form_spray(self):
        form = StockForm(data={'material': self.cleaning_material_spray})
        self.assertTrue(form.is_valid())

    def test_cleaner_stock_form(self):
        form = StockForm(data={'material': 'non_existent_material'})
        self.assertFalse(form.is_valid())

    def test_cleaner_stock_form_all(self):
        form = StockForm(data={'material': ''})
        self.assertTrue(form.is_valid())

    def test_cleaned_room_correct_form(self):
        form = CleanedRoomForm(data={'missing_objects': 'missing_objects',
                                     'need_towels': 2,
                                     'additional_comments': 'additional_comments'})
        self.assertTrue(form.is_valid())

    def test_cleaned_room_correct_form_2(self):
        form = CleanedRoomForm(data={'missing_objects': '',
                                     'need_towels': '',
                                     'additional_comments': ''})
        self.assertTrue(form.is_valid())

    def test_cleaned_room_incorrect_form(self):
        form = CleanedRoomForm(data={'missing_objects': 'missing_objects',
                                     'need_towels': True,
                                     'additional_comments': 'additional_comments'})
        self.assertFalse(form.is_valid())


class TestCleanerViews(BaseTest):

    def test_cleaner_empty_stock(self):
        self.stock_esponja.is_active = False
        self.stock_esponja.save()
        self.stock_spray.is_active = False
        self.stock_spray.save()

        url = reverse('cleaner_stock')
        response = self.client.post(url)
        stock = response.context['stock']
        stock = list(stock)
        self.assertListEqual(stock, [])

    def test_cleaner_stock_esponja(self):
        self.stock_spray.is_active = False
        self.stock_spray.save()

        url = reverse('cleaner_stock')
        response = self.client.post(url)
        stock = response.context['stock']
        stock = list(stock)
        self.assertListEqual(stock, [self.stock_esponja])

    def test_cleaner_stock_spray(self):
        self.stock_esponja.is_active = False
        self.stock_esponja.save()

        url = reverse('cleaner_stock')
        response = self.client.post(url)
        stock = response.context['stock']
        stock = list(stock)

        self.assertListEqual(stock, [self.stock_spray])

    def test_cleaner_stock_all(self):
        url = reverse('cleaner_stock')
        response = self.client.post(url)
        stock = response.context['stock']
        stock = list(stock)
        self.assertListEqual(stock, [self.stock_esponja, self.stock_spray])

    def test_cleaned_room(self):
        url = reverse('cleaner_home')
        self.reservation.check_in_active = False
        self.reservation.check_out_active = False
        self.reservation.save()
        response = self.client.get(url)
        occupied_rooms = response.context['occupied_rooms']
        check_out_rooms = response.context['check_out_rooms']


        """self.assertListEqual(list(occupied_rooms), [self.room])
        self.assertListEqual(list(check_out_rooms), [])"""
