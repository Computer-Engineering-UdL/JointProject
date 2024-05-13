from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django import forms
from Reception.models import RoomReservation, Client, Room, Worker
from Restaurant.models import RestaurantReservation, ExternalRestaurantClient
from Restaurant.forms import NewRestaurantReservationForm, AddInternalClientForm, CreateExternalClientForm, \
    get_available_clients
from Restaurant.config import Config as c
from Reception.forms import SearchReservationForm
from Restaurant.views import restaurant_home, new_restaurant_reservation_1, new_restaurant_reservation_2, \
    new_restaurant_reservation_3


class BaseTest(TestCase):

    def setUp(self):
        self.worker = Worker.objects.create_user(
            username='john_worker',
            email='worker@example.com',
            password='testpassword123',
            type='restaurant'
        )

        self.client_user_is_hosted = Client.objects.create_user(
            username='abde_client',
            email='client@example.com',
            password='clientpassword',
            id_number='12345678A',
            first_name='Abdellah',
            last_name='Lamrani',
            phone_number='123456789',
            is_hosted=True
        )
        self.client_user_not_hosted = Client.objects.create_user(
            username='marc_client',
            email='client_marc@example.com',
            password='clientmarcpassword',
            id_number='12345678A',
            first_name='Marc',
            last_name='Marc',
            phone_number='123356789',
            is_hosted=False
        )

        # ESTO ES LO QUE NECESITO
        self.reservationRestaurant = RestaurantReservation.objects.create(
            client=self.client_user_is_hosted,
            day='2024-12-06',
            num_guests=25,
            service='Dinar'
        )

        self.external_client = ExternalRestaurantClient.objects.create(
            first_name='External1',
            last_name='Client1',
            email='externalclient1@gmail.com',
            phone_number='123456789'
        )

        self.client.force_login(self.worker)


class TestStatusCode(BaseTest):
    def test_restaurant_home_status_code(self):
        url = reverse('restaurant_home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_restaurant_new_reservation_status_code(self):
        url = reverse('restaurant_reservations')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_restaurant_new_reservation_1_status_code(self):
        url = reverse('new_restaurant_reservation_1')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_restaurant_new_reservation_2_status_code(self):
        url = reverse('new_restaurant_reservation_1')
        response = self.client.post(url, {'day': '11/05/2024', 'num_guests': 2, 'service': 'Dinar'})
        self.assertRedirects(response, reverse('new_restaurant_reservation_2'))

        url = reverse('new_restaurant_reservation_2')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_restaurant_new_reservation_3_status_code(self):
        url = reverse('new_restaurant_reservation_1')
        response = self.client.post(url, {'day': '11/05/2024', 'num_guests': 2, 'service': 'Dinar'})
        self.assertRedirects(response, reverse('new_restaurant_reservation_2'))

        url = reverse('new_restaurant_reservation_2')
        response = self.client.post(url, {'client_type': 'internal'})
        self.assertRedirects(response, reverse('new_restaurant_reservation_3'))

        url = reverse('new_restaurant_reservation_3')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestRestaurantForms(BaseTest):
    def test_new_correct_restaurant_reservation_form(self):
        form = NewRestaurantReservationForm(data={'day': '11/05/2024', 'num_guests': 2, 'service': 'Dinar'})
        self.assertTrue(form.is_valid())

    def test_new_incorrect_day_restaurant_reservation_day_before_current_form(self):
        form = NewRestaurantReservationForm(data={'day': '03/05/2024', 'num_guests': 2, 'service': 'Dinar'})
        self.assertFalse(form.is_valid())
        self.assertTrue('No es pot reservar per a un dia passat' in form.errors['__all__'])

    def test_new_incorrect_day_restaurant_reservation_one_year_later_form(self):
        form = NewRestaurantReservationForm(data={'day': '05/05/2026', 'num_guests': 2, 'service': 'Dinar'})
        self.assertFalse(form.is_valid())
        self.assertTrue('No es poden fer reserves per a més d\'un any' in form.errors['__all__'])

    def test_new_restaurant_reservation_max_guests_form(self):
        form = NewRestaurantReservationForm(data={'day': '2024-12-06', 'num_guests': 2, 'service': 'Dinar'})
        self.assertFalse(form.is_valid())
        self.assertTrue(
            'El nombre màxim de convidats per aquest dia ha estat superat (disponibles: 0)' in form.errors['__all__'])

    def test_add_internal_client_form(self):
        form = AddInternalClientForm(data={'client': self.client_user_is_hosted})
        self.assertTrue(form.is_valid())

    def test_add_non_internal_client_form(self):
        form = AddInternalClientForm(data={'client': self.client_user_not_hosted})
        self.assertFalse(form.is_valid())

    def test_create_external_client_form(self):
        form = CreateExternalClientForm(
            data={'email': 'externalclient@gmail.com', 'phone_number': '223456789', 'first_name': 'External',
                  'last_name': 'Client'})
        self.assertTrue(form.is_valid())

    def test_create_external_client_form_email_exists(self):
        form = CreateExternalClientForm(
            data={'email': 'externalclient1@gmail.com', 'phone_number': '223456789', 'first_name': 'External',
                  'last_name': 'Client'})
        self.assertFalse(form.is_valid())
        self.assertTrue('Aquest correu electrònic ja està registrat' in form.errors['__all__'])

    def test_create_external_client_form_phone_number_exists(self):
        form = CreateExternalClientForm(
            data={'email': 'externalclient@gmail.com', 'phone_number': '123456789', 'first_name': 'External',
                  'last_name': 'Client'})
        self.assertFalse(form.is_valid())
        self.assertTrue('Aquest telèfon ja està registrat' in form.errors['__all__'])

    def test_create_external_client_form_invalid_phone_number(self):
        form = CreateExternalClientForm(
            data={'email': 'externalclient@gmail.com', 'phone_number': '12345678', 'first_name': 'External',
                  'last_name': 'Client'})
        self.assertFalse(form.is_valid())
        self.assertTrue('El numero de telèfon no és vàlid' in form.errors['__all__'])

    def test_create_external_client_form_invalid_first_name(self):
        form = CreateExternalClientForm(
            data={'email': 'externalclient@gmail.com', 'phone_number': '223456789', 'first_name': 'E',
                  'last_name': 'Client'})
        self.assertFalse(form.is_valid())

        self.assertTrue('El nom no és vàlid' in form.errors['__all__'])

    def test_create_external_client_form_invalid_last_name(self):
        form = CreateExternalClientForm(
            data={'email': 'externalclient@gmail.com', 'phone_number': '223456789', 'first_name': 'External',
                  'last_name': 'C'})
        self.assertFalse(form.is_valid())

        self.assertTrue('El cognom no és vàlid' in form.errors['__all__'])

    def test_create_external_client_form_invalid_email(self):
        form = CreateExternalClientForm(
            data={'email': 'externalclientgmail.com', 'phone_number': '223456789', 'first_name': 'External',
                  'last_name': 'Client'})
        self.assertFalse(form.is_valid())
        self.assertTrue('El correu electrònic no és vàlid' in form.errors['__all__'])

    def test_create_external_client_form_invalid_email_2(self):
        form = CreateExternalClientForm(
            data={'email': 'externalclient@gmailcom', 'phone_number': '223456789', 'first_name': 'External',
                  'last_name': 'Client'})
        self.assertFalse(form.is_valid())
        self.assertTrue('El correu electrònic no és vàlid' in form.errors['__all__'])


class TestRestaurantViews(BaseTest):

    def test_restaurant_home_view_template(self):
        url = reverse('restaurant_home')
        response = self.client.get(url)
        self.assertTemplateUsed(response, c.get_restaurant_home_path(1))

    def test_restaurant_new_reservations_view_1_with_free_tables(self):
        url = reverse('new_restaurant_reservation_1')
        response = self.client.post(url, {'day': '11/12/2024', 'num_guests': 2, 'service': 'Dinar'})
        self.assertRedirects(response, reverse('new_restaurant_reservation_2'))

    def test_restaurant_new_reservations_view_1_non_tables_available(self):
        url = reverse('new_restaurant_reservation_1')
        response = self.client.post(url, {'day': '12/06/2024', 'num_guests': 2, 'service': 'Dinar'})
        self.assertEqual(response.status_code, 200)

    def test_new_restaurant_reservation_2_view_with_internal_client(self):
        url = reverse('new_restaurant_reservation_1')
        response = self.client.post(url, {'day': '12/12/2024', 'num_guests': 2, 'service': 'Dinar'})
        self.assertRedirects(response, reverse('new_restaurant_reservation_2'))

        url = reverse('new_restaurant_reservation_2')
        response = self.client.post(url, {'client_type': 'internal'})
        self.assertRedirects(response, reverse('new_restaurant_reservation_3'))

    def test_new_restaurant_reservation_2_view_with_external_client(self):
        url = reverse('new_restaurant_reservation_1')
        response = self.client.post(url, {'day': '12/12/2024', 'num_guests': 2, 'service': 'Dinar'})
        self.assertRedirects(response, reverse('new_restaurant_reservation_2'))

        url = reverse('new_restaurant_reservation_2')
        response = self.client.post(url, {'client_type': 'external'})
        self.assertRedirects(response, reverse('new_restaurant_reservation_3'))

    def test_new_restaurant_reservation_2_view_without_client(self):
        url = reverse('new_restaurant_reservation_1')
        response = self.client.post(url, {'day': '12/12/2024', 'num_guests': 2, 'service': 'Dinar'})
        self.assertRedirects(response, reverse('new_restaurant_reservation_2'))

        url = reverse('new_restaurant_reservation_2')
        response = self.client.post(url, {'client_type': ''})
        self.assertEqual(response.status_code, 200)

    def test_new_restaurant_reservation_3_view_with_internal_client(self):
        url = reverse('new_restaurant_reservation_1')
        response = self.client.post(url, {'day': '11/05/2024', 'num_guests': 2, 'service': 'Dinar'})
        self.assertRedirects(response, reverse('new_restaurant_reservation_2'))

        url = reverse('new_restaurant_reservation_2')
        response = self.client.post(url, {'client_type': 'internal'})
        self.assertRedirects(response, reverse('new_restaurant_reservation_3'))

        url = reverse('new_restaurant_reservation_3')
        response = self.client.post(url, {'client': self.client_user_is_hosted.id})
        messages = list(response.wsgi_request._messages)
        self.assertIn("S'ha creat la reserva de restaurant amb èxit!", [str(message) for message in messages])
        self.assertRedirects(response, reverse('restaurant_home'))

        reservation = RestaurantReservation.objects.get(day='2024-11-05', num_guests=2, service='Dinar',
                                                        client=self.client_user_is_hosted)
        self.assertIsNotNone(reservation)

    def test_new_restaurant_reservation_3_view_with_external_client(self):
        url = reverse('new_restaurant_reservation_1')
        response = self.client.post(url, {'day': '11/05/2024', 'num_guests': 2, 'service': 'Dinar'})
        self.assertRedirects(response, reverse('new_restaurant_reservation_2'))

        url = reverse('new_restaurant_reservation_2')
        response = self.client.post(url, {'client_type': 'external'})
        self.assertRedirects(response, reverse('new_restaurant_reservation_3'))

        url = reverse('new_restaurant_reservation_3')
        response = self.client.post(url, {'email': 'example1@gmail.com', 'phone_number': '133456789',
                                          'first_name': 'ExternalName', 'last_name': 'ExternalLastName'})

        messages = list(response.wsgi_request._messages)
        self.assertIn("S'ha creat la reserva de restaurant amb èxit!", [str(message) for message in messages])
        self.assertRedirects(response, reverse('restaurant_home'))

        reservation = RestaurantReservation.objects.get(day='2024-11-05', num_guests=2, service='Dinar')
        self.assertIsNotNone(reservation)

        self.assertEqual(reservation.external_client.first_name, 'ExternalName')
        self.assertEqual(reservation.external_client.last_name, 'ExternalLastName')
