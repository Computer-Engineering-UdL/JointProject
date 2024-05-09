import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8000/accounts/login/?next=/")
    page.get_by_label("Username").click()
    page.get_by_label("Username").fill("admin")
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill("admin")
    page.get_by_label("Password").press("Enter")
    page.get_by_role("link", name="RESTAURANT - Home").click()
    page.get_by_role("button", name="Crear nova reserva").click()
    page.locator("#id_day").fill("2024-09-12")
    page.locator("#id_service").select_option("Dinar")
    page.locator("#id_num_guests").select_option("5")
    page.get_by_role("button", name="Continua").click()
    page.get_by_role("button", name="Client Extern").click()
    page.locator("#id_first_name").click()
    page.locator("#id_first_name").press("CapsLock")
    page.locator("#id_first_name").fill("Test name")
    page.locator("#id_first_name").press("Tab")
    page.locator("#id_last_name").press("CapsLock")
    page.locator("#id_last_name").fill("Test surname")
    page.locator("#id_last_name").press("Tab")
    page.locator("#id_email").fill("test")
    page.locator("#id_email").press("Alt+@")
    page.locator("#id_email").press("Alt+@")
    page.locator("#id_email").fill("test")
    page.locator("#id_email").press("Alt+@")
    page.locator("#id_email").fill("test@gmail.com")
    page.locator("#id_email").press("Tab")
    page.locator("#id_phone_number").fill("334455667")
    page.get_by_role("button", name="Crear Reserva").click()
    page.get_by_role("button", name="Consultar estat reserves").click()
    page.locator("div:nth-child(9) > .list-extra > #checkbox-icon > form > label > img").first.click()
    page.locator("ul:nth-child(2) > div:nth-child(7) > .list-extra > #checkbox-icon > form > label > img").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
