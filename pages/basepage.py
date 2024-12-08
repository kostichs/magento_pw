from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = 'https://magento.softwaretestingboard.com/'
        self.page_url = None

    def open_page(self):
        if self.page_url:
            self.page.goto(f'{self.base_url}{self.page_url}')
        else:
            raise NotImplementedError(f'Page {self.base_url}{self.page_url} cannot be opened')

    def find(self, locator):
        return self.page.locator(locator)
