import random
import re
from playwright.sync_api import expect
import pages.locators.collections_page_loc as loc
from pages.basepage import BasePage
from utils.sort_option import SortOption


class CollectionsPage(BasePage):
    def __init__(self, browser):
        super().__init__(browser)
        self.page_url = '/collections/eco-friendly.html'

    def take_a_random_product(self):
        products = self.take_a_list_of_items()
        product_count = products.count()
        random_index = random.randint(0, product_count - 1)
        random_product = products.nth(random_index)

        product_name_locator = random_product.locator(loc.product_name_loc)
        product_name = product_name_locator.text_content()

        price_locator = random_product.locator(loc.product_price_loc)
        product_price = price_locator.text_content()

        return {
            'element': random_product,
            'name': product_name,
            'price': product_price
        }

    def take_a_list_of_items(self):
        return self.page.locator(loc.products_loc)

    def get_count(self):
        initial_count_text = self.find(loc.page_cart_counter_loc).text_content()
        return int(initial_count_text) if initial_count_text.isdigit() else 0

    def add_to_cart(self, size_and_colors=True):
        random_product_info = self.take_a_random_product()
        random_product = random_product_info['element']
        product_name = random_product_info['name'].strip()
        product_price = random_product_info['price']

        if size_and_colors:
            sizes_locator = random_product.locator(loc.product_sizes)
            size_count = sizes_locator.count()
            if size_count > 0:
                random_size_index = random.randint(0, size_count - 1)
                random_size = sizes_locator.nth(random_size_index)
                random_size.click()

            colors_locator = random_product.locator(loc.product_colors)
            color_count = colors_locator.count()
            if color_count > 0:
                random_color_index = random.randint(0, color_count - 1)
                random_color = colors_locator.nth(random_color_index)
                random_color.click()

        random_product.hover()

        add_to_cart_button = random_product.locator(loc.add_to_cart_loc)

        try:
            add_to_cart_button.click()
        except Exception:
            add_to_cart_button.click(force=True)

        if size_and_colors:
            success_message_locator = self.page.locator(loc.success_message_loc)
            expect(success_message_locator).to_be_visible(timeout=10000)
            success_message_text = success_message_locator.locator("div").text_content().strip()
            assert success_message_text.startswith("You added"), f"Unexpected success message: {success_message_text}"
            assert product_name in success_message_text, (
                f"Product name '{product_name}' not found in success message: {success_message_text}"
            )
        else:
            alert_message_locator = self.page.locator(loc.alert_message_loc)
            expect(alert_message_locator).to_be_visible(timeout=10000)
            alert_message_text = alert_message_locator.locator("div").text_content().strip()
            expected_alert_message = "You need to choose options for your item."
            assert alert_message_text == expected_alert_message, f"Unexpected alert message: {alert_message_text}"

        return {
            "name": product_name,
            "price": product_price,
            "size_and_colors": size_and_colors,
        }


    def __verify_product_in_cart(self, product_name, product_price):
        cart_data_block = self.page.locator(loc.cart_data_block_loc)
        expect(cart_data_block).to_be_visible(timeout=10000)

        cart_name_locator = cart_data_block.locator(loc.inside_cart_product_name_loc)
        cart_price_locator = cart_data_block.locator(loc.inside_cart_product_price_loc)

        cart_name = cart_name_locator.text_content().strip()
        cart_price = cart_price_locator.text_content().strip()

        if cart_name == product_name and cart_price == product_price:
            print(f"Product matched: {cart_name}, Price: {cart_price}")
            return True
        return False

    def switch_sorter_to(self, sort_option):
        while True:
            sort_dropdown = self.page.locator(loc.sorter_loc).nth(0)

            selected_value = sort_dropdown.input_value()

            if selected_value != sort_option.value:
                sort_dropdown.select_option(value=sort_option.value)
            else:
                break

        return sort_dropdown

    def __get_all_prices(self):
        all_products = self.take_a_list_of_items()
        product_prices = []

        for index in range(all_products.count()):
            product = all_products.nth(index)
            price = product.locator(".price").text_content().strip()
            product_prices.append(price)

        return product_prices

    def sort_by_price(self):
        sort_select = self.switch_sorter_to(SortOption.PRICE)
        selected_value = sort_select.input_value()
        assert selected_value == SortOption.PRICE.value, f"Expected {SortOption.PRICE.value}, but got {selected_value}"

        products_locator = self.page.locator(loc.products_loc)
        self.page.wait_for_timeout(1000)
        product_count = products_locator.count()
        assert product_count > 0, "No products found after sorting by price"

        prices = self.__get_all_prices()
        assert prices == sorted(prices), "Products are not sorted by price in ascending order"

        descending_button = self.page.locator(loc.descend_ascend_button_loc).nth(0)
        descending_button.click()
        self.page.wait_for_selector(loc.products_loc)
        prices = self.__get_all_prices()
        assert prices == sorted(prices, reverse=True), "Products are not sorted by price in descending order"
