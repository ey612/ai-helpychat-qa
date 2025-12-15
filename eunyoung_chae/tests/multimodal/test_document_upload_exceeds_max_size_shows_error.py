import time
import os
import pytest
from src.config.config import *
from src.utils.helpers import login, setup_driver, logout, get_file_path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

# [DOC_MDL_TC_003] 허용 용량 초과 문서 업로드 시 에러 메시지가 표시되는지 확인

def test_document_upload_exceeds_max_size_shows_error():
    
    # 로그인, 기다려
    driver = setup_driver(EMAIL, PW)
    wait = WebDriverWait(driver, 10)
    
    # [+] 버튼 및 파일 업로드 버튼
    print("[+] 버튼 누르기")
    plus_icon = driver.find_element(By.CSS_SELECTOR, '[data-testid="plusIcon"]')
    plus_icon.click()
    time.sleep(3)
    
    print("[파일 업로드] 버튼 누르기")
    upload_file_btn = driver.find_element(By.XPATH, "//span[text()='파일 업로드']")
    upload_file_btn.click()
    time.sleep(5)
    
    # 큰 파일 경로 지정
    relative_path = '../../src/resources/asserts/files/test_doc_51mb.pdf'

    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path) 
    
    print(f"파일명: {file_name}")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
    
     # 파일 업로드
    print("파일 업로드 중")
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
        pytest.fail("허용 용량 초과 문서 파일 업로드 시 파일 카드가 표시되면 안 됩니다.")
        
    except TimeoutException:
        # 파일 카드가 나타나지 않으면 성공
        pass
    
    
    # 오류 메시지 확인
    try:
        print("오류 메시지 확인 중")
        alert = wait.until(EC.alert_is_present())
        alert_text = alert.text
        print(f"Alert 메시지: {alert_text}")
        
        # "용량" 또는 "크기" 문구가 포함되어 있는지 확인
        if "용량" in alert_text or "크기" in alert_text:
            print("테스트 통과: 허용 용량 초과 오류 메시지 확인됨")
            alert.accept()
        else:
            alert.accept()
            pytest.fail(f"예상과 다른 오류 메시지: {alert_text}")
            
    except TimeoutException:
        print("테스트 실패: 오류 메시지가 나타나지 않음")
        pytest.fail("허용 용량 초과 문서 파일 업로드 시 오류 메시지가 표시되지 않음")
        
    finally:
        driver.quit()
        
        
        
        

