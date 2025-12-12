from pages.login_page import LoginPage
from utils.constants import TEST_LOGIN_ID, TEST_LOGIN_PASSWORD


def test_login_tc_random(driver):
    login_page = LoginPage(driver)
    login_page.login(
        email=TEST_LOGIN_ID,
        password=TEST_LOGIN_PASSWORD,
    )
