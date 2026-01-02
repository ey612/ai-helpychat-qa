import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GnbComponent:

    locators = {
        "account_management": (By.XPATH, "//span[text()='Account Management']"),
        "person_icon": (By.CSS_SELECTOR, '[data-testid="PersonIcon"]'),
        "password_input": (By.CSS_SELECTOR, '[name="password"]'),
        "login_button": (By.XPATH, '//button[text()="Login"]'),
        "logout_button": (By.XPATH, '//p[text()="Logout"]'),
        "language_setting": (By.XPATH, "//span[text()='언어 설정']"),
    }

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def logout(self):
        print("로그아웃 시도")

        # 1. 사용자 아이콘 클릭
        # icon = self.wait.until(EC.element_to_be_clickable(self.person_icon))
        icon = self.wait.until(EC.element_to_be_clickable(self.locators["person_icon"]))
        icon.click()

        # 드롭다운 메뉴가 나타날 때까지 기다려
        self.wait.until(EC.visibility_of_element_located(self.locators["logout_button"]))
        
        # 2. 로그아웃 버튼 클릭
        # ogout_btn = self.wait.until(EC.element_to_be_clickable(self.logout_button))
        logout_btn = self.wait.until(EC.element_to_be_clickable(self.locators["logout_button"]))
        logout_btn.click()

        # 3. 로그아웃 후 Login 버튼 표시 확인
        login_btn = self.wait.until(
            EC.visibility_of_element_located(self.locators["login_button"])
        )
        return login_btn

    def click_person_icon(self):
        personl_icon = self.wait.until(
            EC.element_to_be_clickable(self.locators["person_icon"])
        )
        personl_icon.click()
        return personl_icon
