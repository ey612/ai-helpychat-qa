import time
import os
import pytest
from src.config.config import *
from src.utils.helpers import login, setup_driver, logout, get_file_path, open_file_upload_dialog
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

# [IMG_MDL_TC_002] 미지원 확장자 이미지 업로드 시 에러 메시지가 표시되는지 확인

def test_image_invalid_extensions_shows_error_svg() :
    
     # 1. 로그인, driver 객체
    driver = setup_driver(EMAIL, PW)
    wait = WebDriverWait(driver, 10)
    
    # 2. 이미지 파일 업로드 하기
    open_file_upload_dialog(driver)
    
    # 3. 이미지 파일 경로 지정
    print("업로드 할 SVG 이미지 파일 경로")
    relative_path = '../../src/resources/asserts/images/test_fail.svg'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path) 
    
    # 4. 이미지 파일 업로드
    print("SVG 이미지 파일 업로드 시도 중")
    file_input_element = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    file_input_element.send_keys(file_path)
    time.sleep(5)
    
    # 이미지 파일 첨부 성공 여부 확인 (미리보기가 나타나면 안 됨)
    
    try :
        
        print("SVG 이미지 파일 미리보기 확인 중")
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'img[alt="{file_name}"]'))
        )
        pytest.fail("지원하지 않는 확장자의[.SVG] 이미지 파일 업로드 시 미리보기가 표시되면 안 됩니다.")
        
    except TimeoutException:
        # 미리보기가 나타나지 않으면 성공
        pass
    
    # 업로드 실패 후 오류 메시지가 뜨는지 확인
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
            "지원하지 않는 확장자[.SVG]의 이미지 파일 업로드 시 오류 메시지가 표시되어야 합니다."
        )
        
def test_image_invalid_extensions_shows_error_ico() :
    
    # 1. 로그인, driver 객체
    driver = setup_driver(EMAIL, PW)
    wait = WebDriverWait(driver, 10)
    
    # 2. 이미지 파일 업로드 하기
    open_file_upload_dialog(driver)
    
    # 3. 이미지 파일 경로 지정
    print("업로드 할 ICO 이미지 파일 경로")
    relative_path = '../../src/resources/asserts/images/test_fail.ico'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path) 
    
    # 4. 이미지 파일 업로드
    print("ICO 이미지 파일 업로드 시도 중")
    file_input_element = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    file_input_element.send_keys(file_path)
    time.sleep(5)
    
    # 이미지 파일 첨부 성공 여부 확인 (미리보기가 나타나면 안 됨)
    
    try :
        
        print("ICO 이미지 파일 미리보기 확인 중")
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'img[alt="{file_name}"]'))
        )
        pytest.fail("지원하지 않는 확장자의[.ICO] 이미지 파일 업로드 시 미리보기가 표시되면 안 됩니다.")
        
    except TimeoutException:
        # 미리보기가 나타나지 않으면 성공
        pass
    
    # 업로드 실패 후 오류 메시지가 뜨는지 확인
    try:
        print("오류 메시지 확인 중")
        alert = wait.until(EC.alert_is_present())
        alert_text = alert.text
        print(f"Alert 메시지: {alert_text}")
        
        # "지원하지 않는" 문구가 포함되어 있는지 확인
        assert "지원하지 않는" in alert_text, \
                f"지원하지 않는 확장자[.ICO]에 대한 오류 메시지가 표시되어야 합니다. (실제 메시지: {alert_text})"

        alert.accept()

    except TimeoutException:
        pytest.fail(
            "지원하지 않는 확장자[.ICO]의 이미지 파일 업로드 시 오류 메시지가 표시되어야 합니다."
        )
