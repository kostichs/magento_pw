def test_creation_account(create_account_page):
    create_account_page.open_page()
    create_account_page.fill_in_account_form_properly()


def test_creation_account_with_wrong_confirmation_password(create_account_page):
    create_account_page.open_page()
    create_account_page.fill_in_account_form_properly(password_confirmation=False)


def test_creation_account_with_existed_email(create_account_page, browser):
    create_account_page.open_page()
    create_account_page.fill_in_form_with_mismatching_password()
