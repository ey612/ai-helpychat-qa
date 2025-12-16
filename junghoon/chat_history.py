from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time


class ChatHistoryManager:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open_rename_popup(self, history_text):
        """
        히스토리 메뉴 → 이름 변경 클릭 → 입력창 오픈
        """

        # 1️⃣ 히스토리 텍스트 찾기
        histories = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "p.MuiTypography-root")
            )
        )

        target = None
        for h in histories:
            if history_text in h.text:
                target = h
                break

        if not target:
            print("⚠ 히스토리 항목을 찾지 못했습니다.")
            return

        # 2️⃣ hover 해서 메뉴 버튼 보이게
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", target
        )
        ActionChains(self.driver).move_to_element(target).perform()
        time.sleep(0.5)

        # 3️⃣ 점 3개 메뉴 버튼 클릭
        menu_btn = target.find_element(
            By.XPATH, ".//following::button[1]"
        )
        self.driver.execute_script("arguments[0].click();", menu_btn)
        print("📂 히스토리 메뉴 클릭")

        # 4️⃣ 이름 변경 클릭
        rename_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[text()='이름 변경']")
            )
        )
        rename_btn.click()
        print("✏️ 이름 변경 클릭 완료")

        # 5️⃣ 입력창 열림 확인
        self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='name']")
            )
        )
        print("🖊️ 이름 변경 입력창 오픈 완료")
        
    def rename_history_and_save(self, old_text, new_text):

        """
        1) 기존 히스토리 텍스트(old_text)를 가진 항목의 이름 변경 팝업을 열고
        2) 이름을 new_text로 바꾸고
        3) '저장' 버튼을 눌러 저장한다.
        """

        # 1️⃣ 팝업 열기 (위에서 이미 잘 되던 메서드 사용)
        self.open_rename_popup(old_text)

        # 2️⃣ 입력창 찾기
        name_input = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[name='name']")
            )
        )

        # 3️⃣ 기존 텍스트 지우고 새 텍스트 입력
        name_input.click()                      # input에 포커스
        name_input.send_keys(Keys.CONTROL, "a") # 전체 선택
        name_input.send_keys(Keys.DELETE)       # 전부 삭제
        
        name_input.send_keys(new_text)
        
        # 4️⃣ '저장' 버튼 클릭
        save_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='submit' and normalize-space(text())='저장']")
            )
        )
        save_button.click()
        print("💾 '저장' 버튼 클릭 완료")
        
        