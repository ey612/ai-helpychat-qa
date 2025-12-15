import time
import os
from src.config.config import *
from src.utils.helpers import login, setup_driver, logout, get_file_path, open_file_upload_dialog
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


# [DOC_MDL_TC_001] 지원 확장자 문서가 정상 업로드되는지 확인

def test_document_upload_valid_extension():
     # 1. 로그인
    driver = setup_driver(EMAIL, PW)
    
    # driver 객체 생성
    wait = WebDriverWait(driver, 10)
    
    # 2. 이미지 업로드 업로드 하기
    open_file_upload_dialog(driver)
    
    # ========= 파일 경로 지정 =========
    
    # 업로드 할 이미지 경로
    print("업로드 할 이미지 경로")
    relative_path = '../../src/resources/asserts/files/test_normal.pdf'
    
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path) 
    
    # ========= 파일이 실제로 있는지 확인 ========= 
    
    # 파일명만 추출
    file_name = os.path.basename(file_path)
    print(f"파일명: {file_name}")
    
    # 파일 존재 여부 확인
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
    print(f"파일 존재 확인 완료. 파일 크기: {os.path.getsize(file_path)}bytes")
    
    # ========= 파일이 실제로 있는지 확인 ========= 
    
    # 파일 업로드
    print("파일 업로드 시도 중")
    file_input_element = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    #file_input_element = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
    file_input_element.send_keys(file_path)
    time.sleep(5)
    
    # 파일 첨부 성공 여부 확인 (파일 카드 생성이 나타나면 안 됨)
    
    wait.until(
        EC.presence_of_element_located((By.XPATH, f"//span[text()='{file_name}']"))
    )
    print("파일 카드가 나타남")
    
    # 추가 안정화 대기
    time.sleep(3)  
    
    # 테스트 성공 여부 확인
    uploaded_image = driver.find_element(By.XPATH, f"//span[text()='{file_name}']")
    assert uploaded_image.is_displayed(), "업로드된 파일 카드가 화면에 나타나지 않았습니다."
    
  
    print("== 파일 업로드 완료 ==")