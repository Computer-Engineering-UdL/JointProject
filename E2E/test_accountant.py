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

    def test_check_item_without_stock(self):
        self.check_item_without_stock(self.page)

    def test_check_item_with_stock(self):
        self.check_item_with_stock(self.page)

    def test_check_item_using_filter(self):
        self.check_item_using_filter(self.page)

    @staticmethod
    def check_item_without_stock(page: Page):
        page.get_by_role("link", name="COMPTABILITAT - Home").click()
        page.locator("#access-process-buttons").get_by_role("button", name="Material de neteja").click()
        page.locator("label").filter(has_text="Esponja").first.click()
        page.get_by_role("button", name="Actualitzar").click()

    @staticmethod
    def check_item_with_stock(page: Page):
        page.get_by_role("link", name="COMPTABILITAT - Home").click()
        page.locator("#access-process-buttons").get_by_role("button", name="Material de neteja").click()
        page.locator("label").filter(has_text="lejia").first.click()
        page.get_by_role("button", name="Actualitzar").click()

    @staticmethod
    def check_item_using_filter(page: Page):
        page.get_by_role("link", name="COMPTABILITAT - Home").click()
        page.locator("#access-process-buttons").get_by_role("button", name="Material de neteja").click()
        page.locator("#id_material").select_option("144")
        page.get_by_role("button", name="Buscar").click()
        page.locator("label").first.click()
        page.get_by_role("button", name="Actualitzar").click()
