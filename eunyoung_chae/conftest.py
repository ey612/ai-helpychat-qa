

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
import time
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.pages.login_page import LoginPage
from src.pages.main_page import GnbComponent, LanguageSetting
from src.config.config import EMAIL, PW

# ================ 공통 상수 ======================
WAIT_TIMEOUT = 10 
# ================ 공통 상수 ======================


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


@pytest.fixture(scope="function")
def logged_in_korean(driver):
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    print("✔️ 로그인 완료")
    
    wait = WebDriverWait(driver, 10)
    try:
        # person icon이 보일 때까지 대기 (페이지 로드 완료 확인)
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="PersonIcon"]')
        ))
        print("✔️ 페이지 로드 완료")
    except:
        print("⚠️ 페이지 로드 대기 시간 초과")
    
    # 2. 언어 확인
    language_setting = LanguageSetting(driver)
    if not language_setting.is_korean():
        print(f"🔄 언어를 한국어로 변경합니다.. (현재: {language_setting.get_current_language()})")
        
        gnb = GnbComponent(driver)
        gnb.click_person_icon()
        time.sleep(2)
        gnb.click_language_setting()
        language_setting.select_language("한국어(대한민국)")
        driver.refresh()
        time.sleep(1)
        print("✔️ 언어 한국어로 변경 완료")
    else:
        print("✔️ 이미 한국어입니다.")
    
    yield driver
    
    # Teardown
    print("\n🔄 Teardown: 언어 복구 중...")
    time.sleep(0.5)
    
    language_setting = LanguageSetting(driver)
    if not language_setting.is_korean():
        try:
            gnb = GnbComponent(driver)
            gnb.click_person_icon()
            
            wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//span[text()='언어 설정' or text()='Language Settings']")
                )
            )
            time.sleep(0.5)
            
            gnb.click_language_setting()
            language_setting.select_language("한국어(대한민국)")
            
            driver.refresh()
            time.sleep(0.5)
            print("✔️ 한국어로 복구 완료")
        except Exception as e:
            print(f"⚠️ 언어 복구 실패: {e}")