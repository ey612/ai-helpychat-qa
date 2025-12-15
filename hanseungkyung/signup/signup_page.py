from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class SignupPage:
    """회원가입 페이지 관련 공통 기능 클래스"""

    def __init__(self, driver):
        self.wait = WebDriverWait(driver, 10)
        self.driver = driver

    def input_email(self, value: str = ""):
        email_input = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@name='email' or @name='loginId' or @type='email']")
            )
        )
        email_input.send_keys(value)
        return email_input

    def input_password(self, value: str = ""):
        password_input = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@name='password' or @type='password']")
            )
        )
        password_input.send_keys(value)
        return password_input

    def input_name(self, value: str = ""):
        name_input = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//input[@name='name' or @name='fullName' or contains(@placeholder, 'Name')]",
                )
            )
        )
        name_input.send_keys(value)
        return name_input

    def click_term_checkbox(self):
        checkboxes = self.driver.find_elements(
            By.CSS_SELECTOR, "input[type='checkbox']"
        )
        if checkboxes and not checkboxes[0].is_selected():
            checkboxes[0].click()
        return checkboxes

    def click_submit_button(self):
        submit_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[@type='submit'] | //button[contains(., 'Sign up')] | //button[contains(., 'Create account')]",
                )
            )
        )
        submit_button.click()
        return submit_button

    def signup(self, email: str = "", password: str = "", name: str = ""):
        self.input_email(email)
        self.input_password(password)
        self.input_name(name)
        self.click_term_checkbox()
        self.click_submit_button()
        return self.driver
