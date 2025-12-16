# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# import time
# import os


# class LoginPage:
    
#     def __init__(self, driver):
#         self.driver = driver
#         self.wait = WebDriverWait(driver, 10)
    
#     def login (self, EMAIL, PW):
        
#         # 아이디 입력 필드 찾아 입력
#         print('아이디 입력 중')
#         login_email = self.driver.find_element(By.CSS_SELECTOR, '[name="loginId"]')
#         login_email.send_keys(EMAIL)
#         print('아이디 입력 완료')
        
        
#         # 비밀번호 입력 필드 찾아 입력 
#         print('비밀번호 입력 중')
#         login_pw = self.driver.find_element(By.CSS_SELECTOR, '[name="password"]')
#         login_pw.send_keys(PW)
#         print('비밀번호 입력 완료')

#         # 로그인 버튼 클릭
        
#         login_btn = self.driver.find_element(By.XPATH, '//button[text()="Login"]')
#         login_btn.click()
#         time.sleep(2)

#     try:
#         DASHBOARD_ELEMENT = (By.NAME, 'input')
#         self.wait.until(EC.presence_of_element_located(DASHBOARD_ELEMENT))
#         print("로그인 성공 및 대시보드 페이지 로드 확인")
#     except Exception :
#         print("로그인 실패 또는 페이지 로드 시간 초과")



#     # 로그아웃 함수
#     def logout (self):
        
#         try:
            
#             # 1. 사용자 아이콘 클릭 
#             print('사용자 아이콘 클릭 하는 중')
#             personl_con = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="PersonIcon"]')
#             personl_con.click()
#             print('✔️ 사용자 아이콘 클릭 완료')
#             time.sleep(1)
            
#             # 2. 로그아웃 버튼 클릭
#             print('로그아웃 버튼 찾는 중')
#             logout_btn = self.find_element(By.XPATH, '//p[text()="Logout"]')
#             logout_btn.click()
#             print('로그아웃 버튼 클릭 완료')
#             time.sleep(5)
            
#             #3. 로그아웃 후 'Login'버튼 나타나는지 확인 (성공)
#             print('로그아웃 완료 검증 중')
#             login_btn_after_logout = self.find_element(By.XPATH, '//button[text()="Login"]')
            
#             if login_btn_after_logout.is_displayed():
#                 print('✔️ 로그아웃 완료 및 "Login" 버튼 확인')
#                 return True
#             else:
#                 print('❌ "Login" 버튼을 찾았으나 화면에 표시되지 않음')
#                 return False
            
#         except NoSuchElementException as e :
#             print(f"❌ 로그아웃 실패: 검증 요소(버튼)를 찾지 못했습니다. 오류: {e}")
#             return False
            
#         except Exception as e :
#             print(f"로그아웃 실패: {e}")
#             return False
