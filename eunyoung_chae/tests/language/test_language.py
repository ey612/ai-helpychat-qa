import pytest
import time
import re
from src.utils.helpers import *
from src.config.config import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


# [LANG_TC_001] 프로필 메뉴에서 언어 설정 클릭 시 지원 언어 목록이 표시되는지 확인
def test_001_language_menu_shows_supported_languages():
    
    #1. 로그인
    
    # LoginPage 객체 생성
    driver = setup_driver(EMAIL, PW)
    
    # 테스트 로직 실행
    
    # 1. 사용자 아이콘 클릭
    personl_con = driver.find_element(By.CSS_SELECTOR, '[data-testid="PersonIcon"]')
    personl_con.click()
    print('✔️ 사용자 아이콘 클릭 완료')
    time.sleep(1)

    # 2. 언어 설정 클릭
    print('== 언어 설정 클릭 중 ==')
    language_setting = driver.find_element(By.XPATH, "//span[text()='언어 설정']")
    language_setting.click()
    print('✔️ 언어 설정 클릭 완료')
    time.sleep(2)
    

    # 드롭다운 메뉴 확인
    expected_languages = [
        'American English',
        '한국어(대한민국)',
        'ไทย (ไทย)',
        '日本語 (日本)'
    ]

    language_time_xpath_template = "//p[text()='{}']"

    test_passed = True
    for language in expected_languages:
        current_locator = (By.XPATH, language_time_xpath_template.format(language))
        
        try:
            driver.find_element(*current_locator)
            print(f" ✔️ [성공] '{language}' 항목이 확인 되었습니다.")
        except NoSuchElementException:
            print(f"❎ [실패] '{language}' 항목을 찾을 수 없습니다.")
            test_passed = False
    assert test_passed, "모든 언어 항목이 드롭다운에 표시되지 않았습니다."

#[LANG_TC_002] 언어 변경 후 재로그인 시 선택한 언어 설정이 유지되는지 확인
def test_002_language_setting_persists_after_relogin():
    
    driver = setup_driver(EMAIL, PW)
    
    try:
        # 기다려
        wait = WebDriverWait(driver, 10)
        
        # 1. 사용자 아이콘 클릭
        personl_con = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="PersonIcon"]'))
        )
        personl_con.click()
        print('✔️ 사용자 아이콘 클릭 완료')
        time.sleep(2)  # 메뉴가 열릴 시간 확보

        # 2. 언어 설정 클릭
        print('== 언어 설정 클릭 중 ==')
        language_setting = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='언어 설정']"))
        )
        language_setting.click()
        print('✔️ 언어 설정 클릭 완료')
        time.sleep(2)
        
        # 3. 언어 선택 (한국어 -> English)
        language_english = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//p[text()='American English']"))
        )
        language_english.click()
        print("✔️ 한국어 --> 영어로 변경 완료!")
        time.sleep(3)
        
        # 4. 언어 변경 확인 (검증)
        VERIFICATION_TEXT = "Account Management"
        ACCOUNT_MANAGEMENT_XPATH = f"//span[text()='{VERIFICATION_TEXT}']"
        
        account_mgmt_element = wait.until(
            EC.presence_of_element_located((By.XPATH, ACCOUNT_MANAGEMENT_XPATH))
        )
        print(f"✅ 언어 변경 확인 성공: '{VERIFICATION_TEXT}' 텍스트가 화면에서 확인되었습니다.")

        # 5. 새로 고침
        driver.refresh()
        print("✔️ 페이지를 새로고침했습니다.")
        time.sleep(3)
        
        # 6. 로그아웃
        logout_successful = logout(driver)
        assert logout_successful, "로그아웃 실패했습니다."
        print('✔️ 로그아웃 완료')
        time.sleep(3)
        
        # 7. 재로그인
        login_pw = driver.find_element(By.NAME, 'password')
        login_pw.send_keys(PW)
        print('비밀번호 입력 완료')

        # 로그인 버튼 클릭
        wait = WebDriverWait(driver, 10)
        login_btn = driver.find_element(By.XPATH, '//button[text()="Login"]')
        login_btn.click()
        time.sleep(2)
        print('재로그인 완료')
        
        # 8. 언어 변경 유지 확인
        
        wait = WebDriverWait(driver, 10)
        VERIFICATION_TEXT = "Account Management"
        personl_con = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="PersonIcon"]'))
            )
        personl_con.click()
        time.sleep(2)
        
        ACCOUNT_MANAGEMENT_XPATH = f"//span[text()='{VERIFICATION_TEXT}']"
        account_mgmt_element = wait.until(
            EC.presence_of_element_located((By.XPATH, ACCOUNT_MANAGEMENT_XPATH))
        )
        print(f"✅ 재로그인 후 언어 유지 확인 성공!")
        assert account_mgmt_element.is_displayed(), "재로그인 후 언어 설정이 유지되지 않았습니다." 
        
        driver.refresh()
        print("✔️ 페이지를 새로고침했습니다.")
        time.sleep(3) 
        
    finally:
        # 언어 원상복구
        if driver is not None: # 드라이버가 생성되었을 때만 실행
            
            try:
                print("\n== 언어 설정 원상복구 시작 ==")
                
                wait = WebDriverWait(driver, 10)
                
                # 사람 아이콘 클릭
                personl_con = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="PersonIcon"]'))
                )
                personl_con.click()
                time.sleep(2)
                
                # 언어 설정 클릭
                language_setting = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='Language Settings']"))
                )
                language_setting.click()
                time.sleep(2)
                
                # 한국어 선택
                language_korean = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//p[text()='한국어(대한민국)']"))
                )
                language_korean.click()
                time.sleep(2)
                
                print("✅ 한국어 원상복구 완료!")
            
            except Exception as e:
                print(f"⚠️ 언어 설정 원상복구 실패: {e}")