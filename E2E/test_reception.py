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

    def test_create_reservation(self):
        self.create_reservation(self.page)

    def test_filter_by_id(self):
        self.filter_by_id(self.page)

    def test_filter_by_reservation_id(self):
        self.filter_by_reservation_id(self.page)

    def test_filter_room_number(self):
        self.filter_room_number(self.page)

    def test_delete_reservation_from_info(self):
        self.delete_reservation_from_info(self.page)

    def test_confirm_check_in(self):
        self.confirm_check_in(self.page)

    def test_confirm_check_out(self):
        self.confirm_check_out(self.page)

    @staticmethod
    def create_reservation(page: Page) -> None:
        page.get_by_role("link", name="RECEPTION - Home").click()
        page.locator("#access-process-buttons").get_by_role("button", name="Reserves").click()
        page.get_by_role("button", name="Crear nova reserva").click()
        page.locator("#entrada").click()
        page.get_by_role("link", name="28").click()
        page.locator("#sortida").click()
        page.get_by_role("link", name="29").click()
        page.locator("#id_client").select_option("95")
        page.locator("#id_num_guests").click()
        page.locator("#id_num_guests").fill("4")
        page.locator("#id_room_type").select_option("Suite")
        page.locator("#id_pension_type").select_option("Completa")
        page.get_by_role("button", name="Continua").click()
        page.once("dialog", lambda dialog: dialog.dismiss())
        page.get_by_role("button", name="Confirmar").click()

    @staticmethod
    def filter_by_id(page: Page) -> None:
        page.get_by_role("link", name="RECEPTION - Home").click()
        page.locator("#access-process-buttons").get_by_role("button", name="Reserves").click()
        page.get_by_role("button", name="Gestionar reserves").click()
        page.locator("#id_id_number").click()
        page.locator("#id_id_number").fill("83393134X")
        page.get_by_role("button", name="Filtrar").click()
        page.get_by_role("link", name="Editar reserva").first.click()
        page.get_by_role("link", name="Torna a Cercar Reserva").click()

    @staticmethod
    def filter_by_reservation_id(page: Page) -> None:
        page.get_by_role("link", name="RECEPTION - Home").click()
        page.locator("#access-process-buttons").get_by_role("button", name="Reserves").click()
        page.get_by_role("button", name="Gestionar reserves").click()
        page.locator("#id_num_reservation").click()
        page.locator("#id_num_reservation").fill("262")
        page.get_by_role("button", name="Filtrar").click()
        page.get_by_role("link", name="Editar reserva").click()
        page.get_by_role("link", name="Torna a Cercar Reserva").click()

    @staticmethod
    def filter_room_number(page: Page) -> None:
        page.get_by_role("link", name="RECEPTION - Home").click()
        page.locator("#access-process-buttons").get_by_role("button", name="Reserves").click()
        page.get_by_role("button", name="Gestionar reserves").click()
        page.locator("#id_room_num").click()
        page.locator("#id_room_num").fill("505")
        page.get_by_role("button", name="Filtrar").click()
        page.get_by_role("link", name="Editar reserva").click()
        page.get_by_role("link", name="Torna a Cercar Reserva").click()

    @staticmethod
    def delete_reservation_from_info(page: Page) -> None:
        page.get_by_role("link", name="RECEPTION - Home").click()
        page.locator("#access-process-buttons").get_by_role("button", name="Reserves").click()
        page.get_by_role("button", name="Gestionar reserves").click()
        page.locator(".icon > a").first.click()
        page.once("dialog", lambda dialog: dialog.dismiss())
        page.get_by_role("button", name="Eliminar reserva").click()

    @staticmethod
    def confirm_check_in(page: Page) -> None:
        page.get_by_role("link", name="RECEPTION - Home").click()
        page.get_by_role("button", name="Check in").click()
        page.locator("#id_room_num").click()
        page.locator("#id_room_num").fill("505")
        page.get_by_role("button", name="Filtrar").click()
        page.get_by_role("link", name="delete").click()
        page.get_by_role("button", name="Check-in ❭").click()

    @staticmethod
    def confirm_check_out(page: Page) -> None:
        page.get_by_role("link", name="RECEPTION - Home").click()
        page.get_by_role("button", name="Check out").click()
        page.locator("#id_room_num").click()
        page.locator("#id_room_num").fill("505")
        page.get_by_role("button", name="Filtrar").click()
        page.get_by_role("link", name="delete").click()
        page.once("dialog", lambda dialog: dialog.dismiss())
        page.get_by_role("button", name="Check-out ❭").click()
