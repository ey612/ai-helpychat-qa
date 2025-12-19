import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


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

        try:
            # 1. 사용자 아이콘 클릭
            print("사용자 아이콘 클릭 중...")
            icon = self.wait.until(EC.element_to_be_clickable(self.person_icon))
            icon.click()
            print("✔️ 사용자 아이콘 클릭 완료")
            time.sleep(1)

            # 2. 로그아웃 버튼 클릭
            print("로그아웃 버튼 대기 중...")
            logout_btn = self.wait.until(EC.element_to_be_clickable(self.logout_button))
            logout_btn.click()
            print("✔️ 로그아웃 버튼 클릭 완료")

            # 3. 로그아웃 후 Login 버튼 표시 확인
            print("로그아웃 완료 검증 중...")
            login_btn = self.wait.until(
                EC.visibility_of_element_located(self.login_button)
            )

            if login_btn.is_displayed():
                print('✔️ 로그아웃 완료 및 "Login" 버튼 확인')
                return True
            else:
                print('❌ "Login" 버튼을 찾았으나 화면에 표시되지 않음')
                return False

        except TimeoutException:
            print("❌ 로그아웃 실패: 타임아웃")
            return False

        except Exception as e:
            print(f"❌ 로그아웃 실패: {e}")
            return False

    def click_person_icon(self):
        personl_con = self.wait.until(
            EC.element_to_be_clickable(self.locators["person_icon"])
        )
        personl_con.click()
        time.sleep(2)
        return personl_con
