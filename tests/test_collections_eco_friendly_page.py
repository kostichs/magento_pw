def test_add_to_cart(collections_eco_page):
    collections_eco_page.open_page()
    collections_eco_page.add_to_cart()


def test_add_to_cart_without_parameters(collections_eco_page):
    collections_eco_page.open_page()
    collections_eco_page.add_to_cart(size_and_colors=False)


def test_sort_by_price(collections_eco_page):
    collections_eco_page.open_page()
    collections_eco_page.sort_by_price()
