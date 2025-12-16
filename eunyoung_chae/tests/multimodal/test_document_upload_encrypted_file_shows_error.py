import time
import os
import pytest
from src.config.config import *
from src.utils.helpers import login, setup_driver, logout, get_file_path, open_file_upload_dialog
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


# 암호화 문서 업로드 시 에러 메시지가 표시되는지 확인 

def test_document_upload_encrypted_file_shows_error():
    
    # 1. 로그인, driver 객체
    driver = setup_driver(EMAIL, PW)
    wait = WebDriverWait(driver, 10)
    
    # 2. 파일 업로드 창 열기
    open_file_upload_dialog(driver)
    
    # 3. 문서 파일 경로 지정
    print("업로드 할 암호화 문서 파일 경로")
    relative_path = '../../src/resources/asserts/files/test_encrypted.docx'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path) 
    
     # 4. 문서 파일 업로드
    print("암호화 문서 파일 업로드 시도 중")
    file_input_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    file_input_element.send_keys(file_path)
    time.sleep(3)

    
    # 파일 첨부 성공 여부 확인 (파일 카드 생성이 나타나면 안 됨)
    try :
        
        print("파일 카드 생성 여부 확인 중")
        wait.until(
            EC.presence_of_element_located((By.XPATH, f"//span[text()='{file_name}']"))
        )
        pytest.fail("암호화 문서 파일 업로드 시 파일 카드가 표시되면 안 됩니다.")
        
    except TimeoutException:
        # 파일 카드가 나타나지 않으면 성공
        pass
    
    
    # 오류 메시지 확인 (오류 메시지가 노출 되어야 함)
    try:
        print("오류 메시지 확인 중")
        alert = wait.until(EC.alert_is_present())
        alert_text = alert.text
        print(f"Alert 메시지: {alert_text}")
        
        # "용량" 또는 "크기" 문구가 포함되어 있는지 확인
        if "암호화" in alert_text :
            print("테스트 통과: 암호화 안내 오류 메시지 확인됨")
            alert.accept()
        else:
            alert.accept()
            pytest.fail(f"예상과 다른 오류 메시지: {alert_text}")
            
    except TimeoutException:
        print("테스트 실패: 오류 메시지가 나타나지 않음")
        pytest.fail("암호화 문서 파일 업로드 시 오류 메시지가 표시되지 않음")