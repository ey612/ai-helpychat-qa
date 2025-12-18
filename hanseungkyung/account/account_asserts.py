# account/account_asserts.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from account.account_page import AccountPage


class AccountAsserts:
    def __init__(self, driver, timeout=25):
        self.wait = WebDriverWait(driver, timeout)

    def assert_saved_successfully(self):
        toast = self.wait.until(EC.visibility_of_element_located(AccountPage.TOAST_SAVED))
        assert "Saved successfully" in toast.text

    def assert_password_format_error(self):
        err = self.wait.until(EC.visibility_of_element_located(AccountPage.PW_FORMAT_ERROR))
        assert err.is_displayed()
