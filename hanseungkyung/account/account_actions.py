from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from account.account_page import AccountPage


class AccountActions:
    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def _wait_account_page_loaded(self):
        """
        계정관리(accounts.elice.io) 페이지 진입 완료 대기
        """
        self.wait.until(EC.url_contains("accounts.elice.io"))
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1 | //h2 | //div[contains(text(),'기본 정보')]")
            )
        )

    def change_name(self, new_name: str):
        # 1️⃣ 계정관리 페이지 로딩 완료 보장
        self._wait_account_page_loaded()

        # 2️⃣ 이름 연필 아이콘 클릭
        try:
            edit_btn = self.wait.until(
                EC.element_to_be_clickable(AccountPage.NAME_EDIT_BTN)
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", edit_btn)
            edit_btn.click()
        except TimeoutException:
            raise AssertionError(
                "이름 연필 아이콘을 찾지 못함: 계정관리 페이지 진입 여부 또는 locator 확인 필요"
            )

        # 3️⃣ 이름 입력
        name_input = self.wait.until(
            EC.visibility_of_element_located(AccountPage.NAME_INPUT)
        )
        name_input.clear()
        name_input.send_keys(new_name)

        # 4️⃣ 완료 버튼 클릭
        save_btn = self.wait.until(
            EC.element_to_be_clickable(AccountPage.SAVE_BTN)
        )
        save_btn.click()
