import pytest
from playwright.sync_api import BrowserContext

from pages.account_creation_page import CreationAccount
from pages.collections_page import CollectionsPage
from pages.sale_page import SalePage


@pytest.fixture()
def page(context: BrowserContext, playwright):
    playwright.selectors.set_test_id_attribute("id")
    page = context.new_page()
    page.set_viewport_size({'width': 1920, 'height': 1080})
    return page


@pytest.fixture
def create_account_page(page):
    return CreationAccount(page)


@pytest.fixture()
def collections_eco_page(page):
    return CollectionsPage(page)


@pytest.fixture()
def sale_page(page):
    return SalePage(page)
