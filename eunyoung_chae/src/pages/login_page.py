from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    
    locators = {
        "email_input": (By.CSS_SELECTOR, '[name="loginId"]'),
        "password_input": (By.CSS_SELECTOR, '[name="password"]'),
        "login_button": (By.XPATH, '//button[text()="Login"]'),
    }
    
    
    def __init__(self,driver):
        
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def login (self, PW, user_id=None):
        """"
        - user_id가 있으면 이메일 + 비밀번호 입력
        - user_id가 없으면 비밀번호만 입력
        """
        print("로그인 시도")

        if user_id:
            print(f"이메일 입력: {user_id}")
            email_el = self.wait.until(EC.presence_of_element_located(self.locators["email_input"]))
            email_el.clear()
            email_el.send_keys(user_id)
        
        print("비밀번호 입력")
        pw_el = self.wait.until(EC.presence_of_element_located(self.locators["password_input"]))
        pw_el.clear()
        pw_el.send_keys(PW)

        print("로그인 버튼 클릭")
        self.wait.until(EC.element_to_be_clickable(self.locators["login_button"])).click()
        print('로그인 버튼 클릭 완료')