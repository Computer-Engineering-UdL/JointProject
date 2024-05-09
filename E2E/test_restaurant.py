import re
from playwright.sync_api import Page, expect


def test_has_title(page: Page):
    page.goto("http://localhost:8000/accounts/login/?next=/")
    page.get_by_label("Username").click()
    page.get_by_label("Username").fill("admin")
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill("admin")
    page.get_by_role("button", name="Submit").click()
    page.get_by_role("link", name="RESTAURANT - Home").click()
    page.get_by_role("button", name="Crear nova reserva").click()
    page.locator("#id_day").fill("2024-05-10")
    page.get_by_role("button", name="Continua").click()
