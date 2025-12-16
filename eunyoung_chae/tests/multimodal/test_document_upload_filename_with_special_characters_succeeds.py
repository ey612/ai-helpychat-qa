import time
import os
from src.config.config import *
from src.utils.helpers import login, setup_driver, logout, get_file_path, open_file_upload_dialog
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


# 특수문자가 포함된 문서 파일명 업로드 시 정상 업로드 확인

def test_document_upload_filename_with_special_characters_succeeds():
    
    # 1. 로그인, driver 객체
    driver = setup_driver(EMAIL, PW)
    wait = WebDriverWait(driver, 10)
    
    # 2. 파일 업로드 창 열기
    open_file_upload_dialog(driver)
    
    # 3. 문서 파일 경로 지정
    print("업로드 할 특수문자 포함된 파일명 문서 파일 경로")
    relative_path = '../../src/resources/asserts/files/test_한글@#$.pdf'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path) 
    
    # 4. 문서 파일 업로드
    print("특수문자 포함된 파일명 문서 파일 업로드 시도 중")
    file_input_element = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    file_input_element.send_keys(file_path)
    time.sleep(5)
    
    # 5. 문서 파일 업로드 확인
    wait.until(
        EC.presence_of_element_located((By.XPATH, f"//span[text()='{file_name}']"))
    )
    print("파일 카드가 나타남")
    
    # 추가 안정화 대기
    time.sleep(3)  
    
    # 테스트 성공 여부 확인
    uploaded_image = driver.find_element(By.XPATH, f"//span[text()='{file_name}']")
    assert uploaded_image.is_displayed(), "업로드된 특수문자 포함된 파일명 문서 파일 카드가 화면에 나타나지 않았습니다."
    print("== 특수문자 포함된 파일명 문서 파일 업로드 완료 ==")
