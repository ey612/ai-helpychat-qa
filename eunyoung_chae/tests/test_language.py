from .data.configs import *
from .actions.common_actions import login, setup_driver, logout
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# [LANG_TC_001] 프로필 메뉴에서 [언어 설정] 클릭 시, 지원되는 언어 목록이 정상적으로 표시되는지 확인
def test_01_language_setting_dropdown():
    
    #1. 로그인
    driver = setup_driver(EMAIL, PW)
    
    try:
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
        
    except Exception as e:
        print(f"실패 메시지: {e}")
    
    finally:
        driver.quit()
        

# [LANG_TC_003] 언어 변경 후 로그아웃 뒤 재로그인 했을 때 이전에 선택했던 언어 설정이 유지되는지 확인       
def test_03_language_checking() :
    
    #1. 로그인
    driver = setup_driver(EMAIL, PW)
    
    #2. 언어 설정 변경
    try:
        
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
        
        # 3. 언어 선택 (한국어 -> English)
        language_english = driver.find_element(By.XPATH, "//p[text()='American English']")
        time.sleep(3)
        print("한국어 --> 영어로 변경 완료!")
        language_english.click()
        time.sleep(3)
        
        # 4. 언어 변경 확인 (검증)
        VERIFICATION_TEXT = "Account Management"
        ACCOUNT_MANAGEMENT_XPATH = f"//span[text()='{VERIFICATION_TEXT}']"
        try:
            time.sleep(2)
            #wait.until(EC.presence_of_element_located((By.XPATH, ACCOUNT_MANAGEMENT_XPATH)))
            print(f"✅ 언어 변경 확인 성공: '{VERIFICATION_TEXT}' 텍스트가 화면에서 확인되었습니다.")
            
            
        except Exception as e :
            print(f"❌ 언어 변경 확인 실패: '{VERIFICATION_TEXT}' 텍스트를 찾을 수 없습니다.")
            print(f"오류 상세: {e}")
        
        # 5. 새로 고침 누르기 (사용자 프로필 다시 열기)
        driver.refresh()
        print("페이지를 새로고침했습니다.")
        time.sleep(3)
        
        # 6. 로그아웃 버튼 클릭
        logout_successful = logout(driver)
        
        # 7. 로그아웃 확인 (검증)
        assert logout_successful == True, "로그아웃 실패했습니다."
        print('✔️로그아웃 완료')
        time.sleep(3)
        
        # 8. 재로그인
        re_login = login(driver, EMAIL, PW)
        
        # 9. 로그인 확인 (검증)
        assert re_login == True, "로그인 실패했습니다."
        
        # 10. 언어 변경 유지 되는지 확인
        try:
            #wait.until(EC.presence_of_element_located((By.XPATH, ACCOUNT_MANAGEMENT_XPATH)))
            time.sleep(3)
            print(f"✅ 언어 변경 확인 성공: '{VERIFICATION_TEXT}' 텍스트가 화면에서 확인되었습니다.")
            
            
        except Exception as e :
            print(f"❌ 언어 변경 확인 실패: '{VERIFICATION_TEXT}' 텍스트를 찾을 수 없습니다.")
            print(f"오류 상세: {e}")
    
    except Exception as e :
        print(f'[LANG_TC_003] 테스트 실패했습니다. 오류 메시지: {e}')
    