import time
import os
import pytest
from src.config.config import *
from src.utils.helpers import login, setup_driver, logout
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


#[IMG_MDL_TC_002] 미지원 확장자 이미지 업로드 시 에러 메시지가 표시되는지 확인
def test_upload_image_with_invalid_extensions_shows_error() :
     # 1. 로그인
    driver = setup_driver(EMAIL, PW)
    
    # driver 객체 생성
    wait = WebDriverWait(driver, 10)
    
    # 2. 이미지 업로드 업로드 하기
    
    # [+] 버튼 누르기
    print("[+] 버튼 누르기")
    plus_icon = driver.find_element(By.CSS_SELECTOR, '[data-testid="plusIcon"]')
    plus_icon.click()
    time.sleep(3)
    print("[+] 버튼 클릭 완료")
    
    # [파일 업로드] 버튼 클릭
    print("[파일 업로드] 버튼 누르기")
    upload_file_btn = driver.find_element(By.XPATH, "//span[text()='파일 업로드']")
    upload_file_btn.click()
    time.sleep(5)
    print("[파일 업로드] 버튼 클릭 완료")
    
    # ========= 파일 경로 지정 =========
    
    # 업로드 할 이미지 경로
    print("업로드 할 이미지 경로")
    relative_file_path = '../../src/resources/asserts/images/fakeimage_txt.jpg'
    
    # current_dir 은 'tests' 폴더 경로
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 'tests/data/elice.png' 합치기
    combined_path = os.path.join(current_dir, relative_file_path)
    
    # 최종 이미지 경로 (컴퓨터는 이 경로를 보고 찾아 감) 
    file_path = os.path.abspath(combined_path)
    print(f"계산된 파일 경로: {file_path}")
    
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
    file_input_element = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    #file_input_element = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
    file_input_element.send_keys(file_path)
    time.sleep(5)
    
    # 파일 첨부 성공 여부 확인
    
    try :
        
        print("파일 미리보기 확인 중")
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'img[alt="{file_name}"]'))
        )
        print("테스트 실패: 파일 미리보기 나타남(나타나지 않아야 함)")
        pytest.fail("지원하지 않는 확장자 파일의 미리보기가 나타남")
        
    except TimeoutException:
        print("테스트 통과: 미리보기가 나타나지 않음")
    
    
    
    # 업로드 실패 후 오류 메시지가 뜨는지 확인
    try:
        # alert가 뜰 때까지 최대 5초 대기
        print("alert 대기 중")
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert_text = alert.text
        print(f"alert 메시지: {alert_text}")
        alert.accept()
        
        # alert가 나타났으면 성공
        assert "지원하지 않는" in alert_text or "오류" in alert_text or "실패" in alert_text
        print("테스트 통과: alert 정상적으로 표시됨")
        
    except TimeoutException:
        # alert가 안 뜨면 fail
        print("테스트 실패: alert 표시 되지 않음")
        pytest.fail("업로드 실패 시 alert 메시지가 표시되지 않음")
        
    finally:
        driver.quit()
