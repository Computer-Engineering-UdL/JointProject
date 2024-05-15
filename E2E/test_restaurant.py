import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("http://localhost:8000/accounts/login/?next=/")
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill("admin")
    page.get_by_role("button", name="Submit").click()
    page.goto("http://localhost:8000/restaurant/")
