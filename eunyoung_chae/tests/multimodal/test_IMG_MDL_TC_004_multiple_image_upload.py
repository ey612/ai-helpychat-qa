import time
import os
from src.config.config import *
from src.utils.helpers import login, setup_driver, logout
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


# [IMG_MDL_TC_004] 여러 이미지를 동시에 업로드 시 정상적으로 업로드 되는지 확인

def test_multiple_image_upload() :
     
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
    
    # 업로드 할 파일 목록
    file_names_to_upload = [
        
        'IMG_MDL_TC_004_1.jpg',
        'IMG_MDL_TC_004_2.jpg'
    ]
    
    # current_dir
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_paths_list = []
    
    # 최종 경로 합치기
    print("== 각 파일의 경로를 계산하고 존재 여부를 확인합니다 ==")
    for file_name in file_names_to_upload:
        
        # 상대 경로 설정
        relative_file_path = f'../../src/resources/asserts/images/{file_name}'

       # 최종 이미지 경로 (컴퓨터는 이 경로를 보고 찾아 감) 
        combined_path = os.path.join(current_dir, relative_file_path)
        file_path = os.path.abspath(combined_path)
        print(f"계산된 파일 경로: {file_path}")
    
    # ========= 파일이 실제로 있는지 확인 ========= 
    
    # 파일 존재 여부 확인
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
        
        file_paths_list.append(file_path)
    
    files_to_send = '\n'.join(file_paths_list)
    print(f"Selenium에 전송할 문자열:\n{files_to_send}")
    
    # ========= 파일이 실제로 있는지 확인 =========    
    
    # 파일 업로드
    file_input_element = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    file_input_element.send_keys(files_to_send)
    time.sleep(5)
    print("== 다중 파일 업로드 요청 완료 ==")
    
    # 파일 첨부 성공 여부 확인
    
    for file_name in file_names_to_upload:
    # 파일명(file_name)을 alt 속성값으로 갖는 img 태그가 나타날 때까지 대기
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'img[alt="{file_name}"]'))
        )
        print(f"{file_name} 파일 미리보기 나타남 확인")
    
    # 추가 안정화 대기
    time.sleep(3)  
    
    # 테스트 성공 여부 확인
    uploaded_image = driver.find_element(By.CSS_SELECTOR, f'img[alt="{file_name}"]')
    assert uploaded_image.is_displayed(), "업로드된 파일 미리보기 이미지가 화면에 나타나지 않았습니다."
    
  
    print("== 파일 업로드 완료 ==")