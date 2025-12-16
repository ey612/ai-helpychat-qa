import time
import os
import pytest
from src.config.config import *
from src.utils.helpers import login, setup_driver, logout, get_file_path, open_file_upload_dialog
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

# 경계값 용량 이미지 업로드 (49MB / 49.9MB)

def test_image_upload_boundary_size_49mb_succeeds():
    # 1. 로그인, driver 객체
    driver = setup_driver(EMAIL, PW)
    wait = WebDriverWait(driver, 10)
    
    # 2. 이미지 파일 업로드 하기
    open_file_upload_dialog(driver)
    
    # 3. 이미지 파일 경로 지정
    print("업로드 할 49MB 이미지 파일 경로")
    relative_path = '../../src/resources/asserts/images/test_49mb.jpg'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path)

    
    # 4. 이미지 파일 업로드
    print("49MB 이미지 파일 업로드 시도 중")
    file_input_element = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    file_input_element.send_keys(file_path)
    time.sleep(5)
    
    # 5. 업로드 확인
    print("49MB 이미지 파일 미리보기 확인 중")
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f'img[alt="{file_name}"]'))
    )
    print("49MB 이미지 파일 미리보기 나타남")
    
    # 추가 안정화 대기
    time.sleep(3)  
    
    # 테스트 성공 여부 확인
    uploaded_image = driver.find_element(By.CSS_SELECTOR, f'img[alt="{file_name}"]')
    assert uploaded_image.is_displayed(), "업로드된 49MB 이미지 파일 미리보기가 화면에 나타나지 않았습니다."
    print("== 49MB 이미지 파일 업로드 완료 ==")

def test_image_upload_boundary_size_49_9mb_succeeds():
      # 1. 로그인, driver 객체
    driver = setup_driver(EMAIL, PW)
    wait = WebDriverWait(driver, 10)
    
    # 2. 이미지 파일 업로드 하기
    open_file_upload_dialog(driver)
    
    # 3. 이미지 파일 경로 지정
    print("업로드 할 49.9MB 이미지 파일 경로")
    relative_path = '../../src/resources/asserts/images/test_49.9mb.jpg'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path)

    
    # 4. 이미지 파일 업로드
    print("49.9MB 이미지 파일 업로드 시도 중")
    file_input_element = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    file_input_element.send_keys(file_path)
    time.sleep(5)
    
    # 5. 업로드 확인
    print("49.9MB 이미지 파일 미리보기 확인 중")
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f'img[alt="{file_name}"]'))
    )
    print("49.9MB 이미지 파일 미리보기 나타남")
    
    # 추가 안정화 대기
    time.sleep(3)  
    
    # 테스트 성공 여부 확인
    uploaded_image = driver.find_element(By.CSS_SELECTOR, f'img[alt="{file_name}"]')
    assert uploaded_image.is_displayed(), "업로드된 49.9MB 이미지 파일 미리보기가 화면에 나타나지 않았습니다."
    print("== 49.9MB 이미지 파일 업로드 완료 ==")