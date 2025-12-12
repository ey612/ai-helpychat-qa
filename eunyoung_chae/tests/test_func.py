from .data.configs import *
from .actions.common_actions import login, setup_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


# 로그인 성공 함수
#def test_initial_login_success(driver):
    # '''로그인 잘 되는지 확인하는 테스트'''

    # print('로그인 시도 중')
    
    # #1. login 함수 실행
    # login(driver, EMAIL, PW)
    
    # # 로그인 검증
    # try:
    #     personl_con = driver.find_element(By.CSS_SELECTOR, '[data-testid="PersonIcon"]')
    #     personl_con.click()
    #     time.sleep(3)
    #     email_display_locator = f"//p[text()='{EMAIL}']"
    #     email_display_element = driver.find_element(By.XPATH, email_display_locator)
    #     #logout_btn = driver.find_element(By.XPATH, "//p[text()='로그아웃']")
    #     print('로그인 성공')
    #     assert email_display_element.is_displayed()
    
    # except Exception as e :
    #     print (f"❌ 로그인 검증 실패: {e}")
    #     assert False, "로그인 후 예상 요소를 찾지 못했습니다."

# 언어 설정 확인
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







