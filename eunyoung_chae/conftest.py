

# 환경 설정

# ==========================================================
# 1. 경로 문제 해결 코드 (이전에 추가했던 내용)
# ==========================================================


import sys
from pathlib import Path

# 프로젝트 루트 디렉토리를 Python path에 추가
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))


# ==========================================================
# 2. WebDriver 및 Pytest Fixture 코드
# ==========================================================


# from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from src.utils.helpers import login, logout
import time
import os
import pytest


# ================ 공통 상수 ======================
WAIT_TIMEOUT = 10 
# ================ 공통 상수 ======================

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

# ================ FIXTURE (드라이버 설정) ======================

@pytest.fixture(scope="function")
def driver() :
    '''테스트 세션 동안 사용할 Chrome WebDriver 생성 및 종료'''

    #1. 크롬 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    #2. 드라이버 생성
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    #3. 드라이버 초기 설정
    driver.implicitly_wait(WAIT_TIMEOUT)
    
    #4. 사이트 접속
    driver.get("https://qaproject.elice.io/ai-helpy-chat")
    time.sleep(3)
    print('✔️ 사이트 접속 완료 (conftest.py)')
    
    # yield : 태스트 함수들에게 설정된 드라이버 객체를 제공
    yield driver
    
    #5. 테스트 종료 후 정리 (Teardown)
    '''모든 테스트가 끝난 후 브라우저 창 닫기'''
    print('\n WebDriver 종료 중 ...')
    driver.quit()