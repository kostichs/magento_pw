import random
import pages.locators.sale_page_loc as loc
from pages.basepage import BasePage


class SalePage(BasePage):
    def __init__(self, browser):
        super().__init__(browser)
        self.page_url = '/sale.html'

    def open_random_link(self):
        links = self.page.locator(loc.links_loc).all()
        while True:
            random_link = random.choice(links)
            href = random_link.get_attribute("href")
            if href:
                break

        self.page.context.new_page()
        new_page = self.page.context.pages[-1]
        new_page.goto(href)

        yield
        new_page.close()

    def open_all_sale_offers(self):
        try:
            links = self.page.locator(loc.links_loc).all()
            for link in links:
                href = link.get_attribute("href")
                if href:
                    new_page = self.page.context.new_page()
                    new_page.goto(href)
                    new_page.locator(loc.page_title_wrapper_loc).wait_for(timeout=10000)

                    title_element = new_page.locator(loc.page_title_heading_loc)
                    title_text = title_element.text_content().strip()

                    href_part = href.split('/')[-1].replace('.html', '')
                    href_word_part = href_part.split('-')[0]

                    assert href_word_part.lower() in title_text.lower(), f'{title_text} does not match for: {href}'
                    new_page.close()

        except Exception as e:
            print(f"An error occurred: {e}")

    def check_title(self):
        page_heading = self.page.locator(loc.page_title_heading_loc).text_content().strip()
        page_title = self.page.title()
        assert page_title == page_heading, f"Title {page_title} does not match heading {page_heading}"

    def validate_promo_links(self):
        promo_links = self.page.locator(loc.links_loc)
        link_count = promo_links.count()
        assert link_count > 0, "No promo links found on the Sale page."
        valid_link_count = 0
        for i in range(link_count):
            link = promo_links.nth(i)
            href = link.get_attribute("href")
            if href:
                valid_link_count += 1
                print(f"Promo link {i + 1} has href: {href}")
            else:
                print(f"Promo link {i + 1} is missing href attribute.")
        assert valid_link_count > 0, "No valid promo links with href attribute found on the Sale page."
