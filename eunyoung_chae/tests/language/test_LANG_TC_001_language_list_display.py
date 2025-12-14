import pytest
import time
import re
from src.config.config import *
from src.utils.helpers import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

# [LANG_TC_001] 프로필 메뉴에서 [언어 설정] 클릭 시, 지원되는 언어 목록이 정상적으로 표시되는지 확인
def test_01_language_list_display():
    
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
    
    finally:
        driver.quit()