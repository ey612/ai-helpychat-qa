from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
import time
import os

# 로그인 함수
def login (driver, EMAIL, PW):
    
    # 아이디 입력 필드 찾아 입력
    print('아이디 입력 중')
    login_email = driver.find_element(By.CSS_SELECTOR, '[name="loginId"]')
    login_email.send_keys(EMAIL)
    print('아이디 입력 완료')
    
    
    # 비밀번호 입력 필드 찾아 입력 
    print('비밀번호 입력 중')
    login_pw = driver.find_element(By.CSS_SELECTOR, '[name="password"]')
    login_pw.send_keys(PW)
    print('비밀번호 입력 완료')

    # 로그인 버튼 클릭
    
    login_btn = driver.find_element(By.XPATH, '//button[text()="Login"]')
    login_btn.click()
    time.sleep(2)

# 로그아웃 함수
def logout (driver):
    
    try:
        
        # 1. 사용자 아이콘 클릭 
        print('사용자 아이콘 클릭 하는 중')
        personl_con = driver.find_element(By.CSS_SELECTOR, '[data-testid="PersonIcon"]')
        personl_con.click()
        print('✔️ 사용자 아이콘 클릭 완료')
        time.sleep(1)
        
        # 2. 로그아웃 버튼 클릭
        print('로그아웃 버튼 찾는 중')
        logout_btn = driver.find_element(By.XPATH, '//p[text()="Logout"]')
        logout_btn.click()
        print('로그아웃 버튼 클릭 완료')
        time.sleep(5)
        
        #3. 로그아웃 후 'Login'버튼 나타나는지 확인 (성공)
        print('로그아웃 완료 검증 중')
        login_btn_after_logout = driver.find_element(By.XPATH, '//button[text()="Login"]')
        
        if login_btn_after_logout.is_displayed():
            print('✔️ 로그아웃 완료 및 "Login" 버튼 확인')
            return True
        else:
            print('❌ "Login" 버튼을 찾았으나 화면에 표시되지 않음')
            return False
        
    except NoSuchElementException as e :
        print(f"❌ 로그아웃 실패: 검증 요소(버튼)를 찾지 못했습니다. 오류: {e}")
        return False
        
    except Exception as e :
        print(f"로그아웃 실패: {e}")
        return False


# 브라우저 여는 함수

WAIT_TIMEOUT = 5
URL = "https://qaproject.elice.io/ai-helpy-chat"

def setup_driver(EMAIL, PW):
    '''브라우저를 열고 기본 설정을 한 뒤 로그인까지 완료하는 헬퍼 함수'''
    
    # 크롬 옵션 정의
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    
    # 드라이버 생성 및 설정 로직
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(WAIT_TIMEOUT)
    driver.get(URL)
    
    # 로그인 함수 호출
    login(driver, EMAIL, PW)
    
    return driver

# 파일 업로드 함수

def get_file_path(relative_path):
    
    
    # current_dir = 현재 위치
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 파일 경로 합치기
    combined_path = os.path.join(current_dir, relative_path)
    
    # 최종 이미지 경로 (컴퓨터는 이 경로를 보고 찾아 감) 
    file_path = os.path.abspath(combined_path)
    print(f"계산된 파일 경로: {file_path}")
    
    file_name = os.path.basename(file_path)
    print(f"파일명: {file_name}")
    
    # 파일 존재 여부 확인
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
    print(f"파일 존재 확인 완료. 파일 크기: {os.path.getsize(file_path)}bytes")
    
    return file_path

def open_file_upload_dialog(driver):
    
    # [+] 버튼 누르기
    print("[+] 버튼 누르기")
    plus_icon = driver.find_element(By.CSS_SELECTOR, '[data-testid="plusIcon"]')
    plus_icon.click()
    time.sleep(3)
    print("[+] 버튼 클릭 완료")
    
    # [파일 업로드] 버튼 클릭
    print("[파일 업로드] 버튼 누르기")
    upload_file_btn = driver.find_element(By.XPATH, "//span[text()='파일 업로드']")
    upload_file_btn.click()
    time.sleep(5)
    print("[파일 업로드] 버튼 클릭 완료")