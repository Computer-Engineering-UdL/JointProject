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

    @staticmethod
    def login(page: Page) -> None:
        page.goto("http://localhost:8000/accounts/login/?next=/")
        page.get_by_label("Username").click()
        page.get_by_label("Username").fill("admin")
        page.get_by_label("Password").click()
        page.get_by_label("Password").fill("admin")
        page.get_by_role("button", name="Submit").click()

    def test_create_restaurant_order(self):
        self.create_reservation_intern_client(self.page)

    def test_create_restaurant_order_external_client(self):
        self.create_reservation_external_client(self.page)

    def test_confirm_reservation(self):
        self.confirm_reservation(self.page)

    def test_delete_reservation(self):
        self.delete_reservation(self.page)

    def test_revert_confirmed_reservation(self):
        self.revert_confirmed_reservation(self.page)

    def test_delete_confirmed_reservation(self):
        self.delete_confirmed_reservation(self.page)

    @staticmethod
    def create_reservation_intern_client(page: Page):
        page.get_by_role("link", name="RESTAURANT - Home").click()
        page.locator("#access-process-buttons").get_by_role("button", name="Nova reserva").click()
        page.locator("#id_num_guests").select_option("4")
        page.get_by_role("button", name="Continua").click()
        page.get_by_role("button", name="Client Intern").click()
        page.locator("#id_client").select_option("101")
        page.get_by_role("button", name="Confirma").click()

    @staticmethod
    def create_reservation_external_client(page: Page):
        page.get_by_role("link", name="RESTAURANT - Home").click()
        page.locator("#access-process-buttons").get_by_role("button", name="Nova reserva").click()
        page.locator("#id_num_guests").select_option("2")
        page.get_by_role("button", name="Continua").click()
        page.get_by_role("button", name="Client Extern").click()
        page.locator("#id_first_name").click()
        page.locator("#id_first_name").fill("John")
        page.locator("#id_first_name").press("Tab")
        page.locator("#id_last_name").fill("Doe")
        page.locator("#id_last_name").press("Tab")
        page.locator("#id_email").fill("john@doe.com")
        page.locator("#id_email").press("Tab")
        page.locator("#id_phone_number").fill("666888999")
        page.get_by_role("button", name="Confirma").click()

    @staticmethod
    def confirm_reservation(page: Page):
        page.get_by_role("link", name="RESTAURANT - Home").click()
        page.locator("#access-process-buttons").get_by_role("button", name="Reserves").click()
        page.locator("label > img").first.click()

    @staticmethod
    def delete_reservation(page: Page):
        page.get_by_role("link", name="RESTAURANT - Home").click()
        page.locator("#access-process-buttons").get_by_role("button", name="Reserves").click()
        page.once("dialog", lambda dialog: dialog.dismiss())
        page.locator("form > button").first.click()

    @staticmethod
    def revert_confirmed_reservation(page: Page):
        page.get_by_role("link", name="RESTAURANT - Home").click()
        page.locator("#access-process-buttons").get_by_role("button", name="Reserves").click()
        page.locator("ul:nth-child(2) > div:nth-child(4) > .list-extra > #checkbox-icon > "
                     ".check-form > label > img").click()

    @staticmethod
    def delete_confirmed_reservation(page: Page):
        page.get_by_role("link", name="RESTAURANT - Home").click()
        page.locator("#access-process-buttons").get_by_role("button", name="Reserves").click()
        page.once("dialog", lambda dialog: dialog.dismiss())
        page.locator("ul:nth-child(2) > div:nth-child(4) > .list-extra > div:nth-child(2) > form > button").click()
