# account/account_actions.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from account.account_page import AccountPage


class AccountActions:
    def __init__(self, driver, timeout=40):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def _js_click(self, el):
        try:
            el.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", el)

    def _scroll_center(self, el):
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)

    def _switch_to_new_tab_if_opened(self, before_handles):
        try:
            self.wait.until(lambda d: len(d.window_handles) != len(before_handles))
            after = self.driver.window_handles
            new_handle = [h for h in after if h not in before_handles][0]
            self.driver.switch_to.window(new_handle)
        except Exception:
            pass

    def open_account_page(self):
        """
        Helpy Chat 화면에서
        1) 우측 상단 사람(아바타) 클릭
        2) '계정 관리' 클릭
        3) 새 탭 열리면 accounts.elice.io 로 전환
        """
        before = self.driver.window_handles

        avatar = self.wait.until(EC.element_to_be_clickable(AccountPage.AVATAR_BTN))
        self._scroll_center(avatar)
        self._js_click(avatar)

        # 프로필 패널이 열리고 '계정 관리'가 clickable 될 때까지
        link = self.wait.until(EC.element_to_be_clickable(AccountPage.ACCOUNT_MANAGEMENT_LINK))
        self._scroll_center(link)
        self._js_click(link)

        self._switch_to_new_tab_if_opened(before)

        # accounts 페이지 로딩 확인
        self.wait.until(lambda d: "accounts.elice.io" in d.current_url)
        self.wait.until(EC.presence_of_element_located(AccountPage.READY))

    # ======================
    # 이름 변경
    # ======================
    def change_name(self, new_name: str):
        btn = self.wait.until(EC.element_to_be_clickable(AccountPage.NAME_EDIT_BTN))
        self._scroll_center(btn)
        self._js_click(btn)

        inp = self.wait.until(EC.presence_of_element_located(AccountPage.NAME_INPUT))
        self._scroll_center(inp)

        # MUI input: clear() 불안정해서 Ctrl+A 삭제
        inp.click()
        inp.send_keys(Keys.CONTROL, "a")
        inp.send_keys(Keys.BACKSPACE)
        inp.send_keys(new_name)

        # 값 반영 대기 (완료 버튼 활성화 조건)
        self.wait.until(lambda d: (inp.get_attribute("value") or "").strip() == new_name.strip())

        done = self.wait.until(EC.presence_of_element_located(AccountPage.DONE_BTN))
        self.wait.until(lambda d: done.is_enabled())
        self._scroll_center(done)
        self._js_click(done)

        # 저장 토스트 뜨면 성공으로 간주
        self.wait.until(EC.presence_of_element_located(AccountPage.SAVE_TOAST))

    # ======================
    # 비밀번호 변경 (눈 아이콘 순서 반영)
    # ======================
    def _click_eye_for_input(self, input_el):
        """
        input id를 aria-controls로 참조하는 눈(visibility) 버튼을 찾아 클릭.
        """
        input_id = input_el.get_attribute("id") or ""
        if not input_id:
            return

        # 같은 row 안에서 aria-controls가 input_id인 버튼을 찾음
        btn = self.driver.find_elements(By.CSS_SELECTOR, f"button[aria-controls='{input_id}']")
        if btn:
            self._scroll_center(btn[0])
            self._js_click(btn[0])

    def change_password(self, current_pw: str, new_pw: str):
        """
        네가 준 TC 순서 그대로:

        1. 비밀번호 수정 아이콘 클릭
        2. 기존 비밀번호 옆 눈아이콘 누르기
        3. 새 비밀번호 옆 눈아이콘 누르기
        4. 기존 비밀번호 입력
        5. 새 비밀번호 입력
        6. '완료' 클릭
        """
        # 1) 수정 아이콘
        edit = self.wait.until(EC.element_to_be_clickable(AccountPage.PASSWORD_EDIT_BTN))
        self._scroll_center(edit)
        self._js_click(edit)

        # input 로딩 대기
        cur = self.wait.until(EC.presence_of_element_located(AccountPage.CURRENT_PW_INPUT))
        self._scroll_center(cur)

        # 새 비번 input은 화면에 따라 늦게 뜰 수 있음
        try:
            new = self.wait.until(EC.presence_of_element_located(AccountPage.NEW_PW_INPUT))
        except Exception:
            # fallback: password input 중 current-password 제외한 나머지
            pw_inputs = [e for e in self.driver.find_elements(By.CSS_SELECTOR, "input[type='password']") if e.is_displayed()]
            new = None
            for e in pw_inputs:
                if (e.get_attribute("autocomplete") or "").strip() != "current-password":
                    new = e
                    break
            if new is None:
                raise

        # 2) 기존 비번 눈아이콘
        self._click_eye_for_input(cur)

        # 3) 새 비번 눈아이콘
        self._click_eye_for_input(new)

        # 4) 기존 비번 입력
        cur.click()
        cur.send_keys(Keys.CONTROL, "a")
        cur.send_keys(Keys.BACKSPACE)
        cur.send_keys(current_pw)

        # 5) 새 비번 입력
        new.click()
        new.send_keys(Keys.CONTROL, "a")
        new.send_keys(Keys.BACKSPACE)
        new.send_keys(new_pw)

        # 6) 완료 클릭
        done = self.wait.until(EC.presence_of_element_located(AccountPage.DONE_BTN))
        self.wait.until(lambda d: done.is_enabled())
        self._scroll_center(done)
        self._js_click(done)

        self.wait.until(EC.presence_of_element_located(AccountPage.SAVE_TOAST))

    # ======================
    # 프로모션 알림(마케팅) 토글
    # ======================
    def toggle_promotion_marketing(self):
        el = self.wait.until(EC.presence_of_element_located(AccountPage.PROMO_MARKETING))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        self._js_click(el)

        self.wait.until(EC.presence_of_element_located(AccountPage.SAVE_TOAST))
