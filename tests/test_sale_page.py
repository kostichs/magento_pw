def test_sale_links(sale_page):
    sale_page.open_page()
    sale_page.open_all_sale_offers()


def test_validate_promo_links(sale_page):
    sale_page.open_page()
    sale_page.validate_promo_links()


def test_check_title(sale_page):
    sale_page.open_page()
    sale_page.check_title()
