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
        self.room1 = Room.objects.create(
            is_clean=True,
            is_taken=False,
            room_num=202,
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


class CheckInFormsAndRedirectsTest(BaseTest):

    def test_check_in_view_status_code(self):
        url = reverse('check_in')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_check_in_redirect_with_reservation(self):
        url = reverse('check_in')
        response = self.client.post(url, {'num_reservation': self.reservation.id})
        self.assertTemplateUsed(response, c.get_check_in_path(1))

    def test_check_in_redirect_with_id_number(self):
        url = reverse('check_in')
        response = self.client.post(url, {'id_number': self.client_user.id_number})
        self.assertTemplateUsed(response, c.get_check_in_path(1))

    def test_check_in_redirect_with_room_number(self):
        url = reverse('check_in')
        response = self.client.post(url, {'room_num': self.room.room_num})
        self.assertTemplateUsed(response, c.get_check_in_path(1))

    def test_check_in_correct_search_with_reservation(self):
        form = SearchReservationForm(data={'num_reservation': self.reservation.id})
        self.assertTrue(form.is_valid())

    def test_check_in_incorrect_search_with_reservation(self):
        form = SearchReservationForm(data={'num_reservation': '11'})
        self.assertFalse(form.is_valid())
        self.assertTrue('No existeix cap reserva amb aquest número' in form.errors['__all__'])

    def test_check_in_summary_view_status_code(self):
        url = reverse('check_in_summary', args=[self.reservation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

class CheckInViewTest(BaseTest):
    def test_check_in_1_view_exist_reservation(self):
        url = reverse('check_in')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        reservations = response.context['reservations']
        self.assertIn(self.reservation, reservations)

    def test_check_in_1_view_non_exist_reservation(self):
        url = reverse('check_in')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        reservation = RoomReservation.objects.create(
            client=self.client_user,
            room=self.room1,
            entry=timezone.now().date(),
            exit=(timezone.now() + timezone.timedelta(days=1)).date(),
            pension_type='Sense pensió',
            num_guests=1
        )

        reservations = response.context['reservations']
        self.assertNotIn(reservation, reservations)

    def test_check_in_summary_view_with_reservation(self):
        url = reverse('check_in_summary', args=[self.reservation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_check_in_summary_view_with_nonexistent_reservation(self):
        url = reverse('check_in_summary', args=[1])
        response = self.client.get(url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "No s'ha trobat la reserva")


class RoomReservationTest(BaseTest):
    def test_room_reservation(self):
        url = reverse('new_reservation_1')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class CheckOutFormsAndRedirectsTest(BaseTest):
    def test_check_out(self):
        url = reverse('check_out')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # TEST CASES FOR CHECK OUT IN PROCESS
    def test_check_out_view_redirect_with_reservation(self):
        url = reverse('check_out')
        response = self.client.post(url, {'num_reservation': self.reservation.id})
        self.assertTemplateUsed(response, c.get_check_out_path(1))

    def test_check_out_view_redirect_with_id_number(self):
        url = reverse('check_out')
        response = self.client.post(url, {'id_number': self.client_user.id_number})
        self.assertTemplateUsed(response, c.get_check_out_path(1))

    def test_check_out_view_redirect_with_room_number(self):
        url = reverse('check_out')
        response = self.client.post(url, {'room_num': self.room.room_num})
        self.assertTemplateUsed(response, c.get_check_out_path(1))

    def test_check_out_correct_search_with_reservation(self):
        form = SearchReservationForm(data={'num_reservation': self.reservation.id})
        self.assertTrue(form.is_valid())

    def test_check_out_incorrect_search_with_reservation(self):
        form = SearchReservationForm(data={'num_reservation': '11'})
        self.assertFalse(form.is_valid())
        self.assertTrue('No existeix cap reserva amb aquest número' in form.errors['__all__'])

    def test_check_out_correct_search_with_id_number(self):
        form = SearchReservationForm(data={'id_number': self.client_user.id_number})
        self.assertTrue(form.is_valid())

    def test_check_out_incorrect_search_with_id_number(self):
        form = SearchReservationForm(data={'id_number': '12345984B'})
        self.assertFalse(form.is_valid())
        self.assertTrue('No existeix cap client amb aquest número d\'identificació' in form.errors['__all__'])

    def test_check_out_correct_search_with_room_number(self):
        form = SearchReservationForm(data={'room_num': self.room.room_num})
        self.assertTrue(form.is_valid())

    def test_check_out_incorrect_search_with_room_number(self):
        form = SearchReservationForm(data={'room_num': '202'})
        self.assertFalse(form.is_valid())
        self.assertTrue('No existeix cap reserva per aquesta habitació' in form.errors['__all__'])

    def test_check_out_search_with_non_existent_room_number(self):
        form = SearchReservationForm(data={'room_num': '20122'})
        self.assertFalse(form.is_valid())
        self.assertTrue('No existeix cap habitació amb aquest número' in form.errors['__all__'])

    def test_check_out_with_empty_fields(self):
        form = SearchReservationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertTrue('Introdueix informació en algun dels camps per a la cerca' in form.errors['__all__'])

    def test_check_out_incorrect_format_reservation(self):
        form = SearchReservationForm(data={'num_reservation': 'aer'})
        self.assertFalse(form.is_valid())
        self.assertTrue('Introdueix un número de reserva vàlid' in form.errors['__all__'])

    def test_check_out_incorrect_format_id_number(self):
        form = SearchReservationForm(data={'id_number': '33442244rrtes'})
        self.assertFalse(form.is_valid())
        self.assertTrue('Introdueix un número d\'identificació vàlid' in form.errors['__all__'])


class CheckOutViewTest(BaseTest):

    def test_check_out_view_status_code(self):
        url = reverse('check_out')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test
    def test_check_out_3_view_status_code(self):
        url = reverse('check_out_3', args=[self.reservation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    """def test_print_receipt_check_out_view_status_code(self):
        url = reverse('print_receipt_check_out', args=[self.client_user.id, self.reservation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)"""
