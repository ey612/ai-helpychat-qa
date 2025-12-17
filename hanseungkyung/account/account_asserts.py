from account.account_page import AccountPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AccountAsserts:
    def __init__(self, driver):
        self.wait = WebDriverWait(driver, 10)

    def assert_save_success(self):
        toast = self.wait.until(EC.visibility_of_element_located(AccountPage.TOAST))
        assert "저장" in toast.text

    def assert_password_error(self):
        error = self.wait.until(EC.visibility_of_element_located(AccountPage.ERROR_MSG))
        assert "강력" in error.text or "8자" in error.text
