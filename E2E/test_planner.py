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

    def test_assign_cleaning_worker(self):
        self.assign_cleaning_worker(self.page)

    def test_revert_assign_cleaning_worker(self):
        self.revert_assign_cleaning_worker(self.page)

    def test_add_worker(self):
        self.add_worker(self.page)

    def test_add_room(self):
        self.add_room(self.page)

    @staticmethod
    def assign_cleaning_worker(page: Page):
        page.get_by_role("link", name="PLANNER - Home").click()
        page.locator("#access-process-buttons").get_by_role("button", name="Assignacions neteja").click()
        page.get_by_role("button", name="603").click()
        page.get_by_label("Esculli al treballador:").select_option("171")
        page.get_by_role("button", name="Assignar").click()

    @staticmethod
    def revert_assign_cleaning_worker(page: Page):
        page.get_by_role("link", name="PLANNER - Home").click()
        page.locator("#access-process-buttons").get_by_role("button", name="Assignacions neteja").click()
        page.get_by_role("link", name="delete").first.click()
        page.get_by_label("Esculli al treballador:").select_option("178")
        page.get_by_role("button", name="Assignar", exact=True).click()

    @staticmethod
    def add_worker(page: Page):
        page.get_by_role("link", name="PLANNER - Home").click()
        page.get_by_role("button", name="Nou treballador").click()
        page.locator("#id_first_name").click()
        page.locator("#id_first_name").fill("John")
        page.locator("#id_first_name").press("Tab")
        page.locator("#id_last_name").fill("Doe")
        page.locator("#id_last_name").press("Tab")
        page.locator("#id_id_number").fill("83393134X")
        page.locator("#id_email").click()
        page.locator("#id_email").fill("john@doe")
        page.locator("#id_email").press("Tab")
        page.locator("#id_phone_number").fill("555888999")
        page.locator("#id_username").click()
        page.locator("#id_username").fill("johndoe22")
        page.locator("#id_password1").click()
        page.locator("#id_password1").fill("johndoe")
        page.locator("#id_password2").click()
        page.locator("#id_password2").fill("johndoe")
        page.locator("#id_worker_type").select_option("restaurant")
        page.get_by_role("button", name="Confirma").click()

    @staticmethod
    def add_room(page: Page):
        page.get_by_role("link", name="PLANNER - Home").click()
        page.get_by_role("button", name="Afegir habitacions").click()
        page.locator("#id_room_num").click()
        page.locator("#id_room_num").fill("599")
        page.get_by_role("button", name="Confirma").click()
