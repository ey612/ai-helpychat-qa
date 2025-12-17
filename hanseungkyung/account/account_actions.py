# account/account_actions.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from account.account_page import AccountPage


class AccountActions:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def _click_any(self, candidates, name="element"):
        last = None
        for by, value in candidates:
            try:
                el = self.wait.until(EC.presence_of_element_located((by, value)))
                self.wait.until(EC.visibility_of(el))
                # 클릭이 막히는 케이스 대비: 스크롤 + JS 클릭
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                try:
                    el.click()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", el)
                return
            except Exception as e:
                last = e
        raise last if last else Exception(f"Cannot find {name}")

    def open_account_page(self):
        # ✅ 사람 아이콘 클릭
        self._click_any(AccountPage.AVATAR_BTN_CANDIDATES, name="avatar button")

        # ✅ 계정관리 메뉴 클릭
        self._click_any(AccountPage.ACCOUNT_MENU_CANDIDATES, name="account menu")

    def change_name(self, name):
        self.wait.until(EC.element_to_be_clickable(AccountPage.NAME_CHANGE_BTN)).click()
        name_input = self.wait.until(EC.presence_of_element_located(AccountPage.NAME_INPUT))
        name_input.clear()
        name_input.send_keys(name)
        self.wait.until(EC.element_to_be_clickable(AccountPage.SAVE_BTN)).click()

    def change_password(self, current_pw, new_pw):
        self.wait.unt
