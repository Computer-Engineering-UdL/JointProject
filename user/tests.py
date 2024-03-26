from django.test import TestCase
from Reception.models import HotelUser

USERNAME = 'testuser'
EMAIL = 'testuser@testing.com'
PASSWORD = 'testUserPassword1234'


# STATUS CODES:
# 302: Stands for a redirect status code
# 200: Stands for a success status code
# 400: Stands for a bad request status code
# 404: Stands for a not found status code
# 500: Stands for a server error status code

class TestLogin(TestCase):
    def setUp(self):
        self.user = HotelUser.objects.create_user(username=USERNAME, email=EMAIL, password=PASSWORD)

    def test_login(self):
        response = self.client.login(username=USERNAME, password=PASSWORD)
        self.assertTrue(response)

    def test_login_redirect(self):
        response = self.client.post('/accounts/login/', {'username': USERNAME, 'password': PASSWORD})
        self.assertEqual(response.status_code, 302)

    def test_logout_redirect(self):
        response = self.client.post('/accounts/logout/')
        self.assertEqual(response.status_code, 302)


class TestSignup(TestCase):
    def test_signup(self):
        response = self.client.post('/accounts/signup/', {
            'username': USERNAME,
            'email': EMAIL,
            'password1': PASSWORD,
            'password2': PASSWORD
        })
        self.assertEquals(response.status_code, 302)
