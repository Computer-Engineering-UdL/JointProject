from django.test import TestCase
from playwright.sync_api import Page, sync_playwright


class PlaywrightTest(TestCase):
    def setUp(self):
        self.client.login(username='admin', password='admin')
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()
        self.page = self.browser.new_page()
        self.login(self.page)

    def tearDown(self):
        self.browser.close()
        self.playwright.stop()

    def test_create_restaurant_reservation(self):
        self.create_restaurant_reservation(self.page)

    @staticmethod
    def login(page: Page) -> None:
        page.goto("http://localhost:8000/accounts/login/?next=/")
        page.get_by_label("Username").click()
        page.get_by_label("Username").fill("admin")
        page.get_by_label("Password").click()
        page.get_by_label("Password").fill("admin")
        page.get_by_role("button", name="Submit").click()

    @staticmethod
    def create_restaurant_reservation(page: Page) -> None:
        page.get_by_role("link", name="GUESTS - Home").click()
        page.get_by_role("button", name="Reservar taula").click()
        page.locator("#id_day").fill("2024-06-21")
        page.locator("#id_num_guests").select_option("2")
        page.get_by_role("button", name="Continua").click()
        page.locator("#id_id_number").click()
        page.locator("#id_id_number").fill("83393134X")
        page.get_by_role("button", name="Continua").click()
        page.locator("#id_first_name").click()
        page.locator("#id_first_name").fill("John")
        page.locator("#id_last_name").click()
        page.locator("#id_last_name").fill("Doe")
        page.locator("#id_email").click()
        page.locator("#id_email").fill("jonh@doe.com")
        page.locator("#id_email").press("Tab")
        page.locator("#id_phone_number").fill("888999777")
        page.get_by_role("button", name="Confirma").click()
