import time
import os
import pytest
from src.config.config import *
from src.utils.helpers import login, setup_driver, logout, get_file_path, open_file_upload_dialog
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

# [DOC_MDL_TC_002] 미지원 확장자 문서 업로드 시 에러 메시지가 표시되는지 확인

def test_document_invalid_extensions_shows_error() :
     # 1. 로그인
    driver = setup_driver(EMAIL, PW)
    
    # driver 객체 생성
    wait = WebDriverWait(driver, 10)
    
    # 2. 파일 업로드 업로드 하기
    
    open_file_upload_dialog(driver)
    
    # ========= 파일 경로 지정 =========
    
    # 업로드 할 파일 경로
    print("업로드 할 이미지 경로")
    relative_path = '../../src/resources/asserts/files/test_upload_fail.exe'
    
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path) 
    
    
    # ========= 파일이 실제로 있는지 확인 ========= 
    
    # 파일 업로드
    file_input_element = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    #file_input_element = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
    file_input_element.send_keys(file_path)
    time.sleep(5)
    
    # 파일 첨부 성공 여부 확인 (파일 카드 생성이 나타나면 안 됨)
    
    try :
        
        print("파일 카드 생성 확인 중")
        wait.until(
            EC.presence_of_element_located((By.XPATH, f'//span[text()="{file_name}"]'))
        )
        pytest.fail("지원하지 않는 확장자의 문서 파일 업로드 시 파일 카드가 표시되면 안 됩니다.")
        
    except TimeoutException:
        # 파일 카드가 나타나지 않으면 성공
        pass
    
    
    
    # # 업로드 실패 후 오류 메시지가 뜨는지 확인
    try:
        print("오류 메시지 확인 중")
        alert = wait.until(EC.alert_is_present())
        alert_text = alert.text
        print(f"Alert 메시지: {alert_text}")
        
        # "지원하지 않는" 문구가 포함되어 있는지 확인
        assert "지원하지 않는" in alert_text, \
                f"지원하지 않는 확장자에 대한 오류 메시지가 표시되어야 합니다. (실제 메시지: {alert_text})"

        alert.accept()

    except TimeoutException:
        pytest.fail(
            "지원하지 않는 확장자의 문서 파일 업로드 시 오류 메시지가 표시되어야 합니다."
        )

    finally:
        driver.quit()