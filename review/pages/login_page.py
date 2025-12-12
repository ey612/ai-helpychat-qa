from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class LoginPage:
    """로그인 페이지 관련 공통 기능 클래스"""

    def __init__(self, driver):
        self.wait = WebDriverWait(driver, 10)
        self.driver = driver

    def input_email(self, value: str = ""):
        email_input = self.wait.until(
            EC.presence_of_element_located((By.NAME, "loginId"))
        )
        email_input.send_keys(value)
        return email_input

    def input_password(self, value: str = ""):
        password_input = self.wait.until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_input.send_keys(value)
        return password_input

    def click_login_button(self):
        login_button = self.wait.until(EC.element_to_be_clickable((By.ID, ":r3:")))
        login_button.click()
        return login_button

    def login(self, email: str = "", password: str = ""):
        self.input_email(email)
        self.input_password(password)
        self.click_login_button()
        return self.driver
