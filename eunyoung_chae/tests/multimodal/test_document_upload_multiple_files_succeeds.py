import time
import os
from src.config.config import *
from src.utils.helpers import login, setup_driver, logout, get_file_path, open_file_upload_dialog
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


# 여러 문서 동시 업로드 시 정상 업로드되는지 확인

def test_document_upload_multiple_files_succeeds():
    
     # 1. 로그인, driver 객체
    driver = setup_driver(EMAIL, PW)
    wait = WebDriverWait(driver, 10)
    
    # 2. 문서 파일 업로드 하기
    open_file_upload_dialog(driver)
    
    #  3. 문서 파일 경로 지정
    
    print("업로드 할 문서 파일 목록 만들기")
    file_names_to_upload = [
        
        'test_multi_1.pdf',
        'test_multi_2.docx'
    ]
    
    # current_dir
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_paths_list = []
    
    # 최종 경로 합치기
    print("업로드 할 문서 파일 경로 찾기")
    for file_name in file_names_to_upload:
        
        # 상대 경로 설정
        relative_path = f'../../src/resources/asserts/files/{file_name}'

       # 최종 이미지 경로 (컴퓨터는 이 경로를 보고 찾아 감) 
        combined_path = os.path.join(current_dir, relative_path)
        file_path = os.path.abspath(combined_path)
        print(f"계산된 파일 경로: {file_path}")

    
        # 파일 존재 여부 확인
        print("문서 파일이 존재 하는지 확인하는 중")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
        
        # 파일 경로를 리스트에 추가
        file_paths_list.append(file_path)
    
    files_to_send = '\n'.join(file_paths_list)
    print(f"Selenium에 전송할 문자열:\n{files_to_send}")
    
    # 4. 문서 파일 업로드
    file_input_element = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    file_input_element.send_keys(files_to_send)
    time.sleep(5)
    print("== 다중 파일 업로드 요청 완료 ==")
    
    # 문서 파일 첨부 성공 여부 확인
    
    for file_name in file_names_to_upload:
        
        wait.until(
            EC.presence_of_element_located((By.XPATH, f"//span[text()='{file_name}']"))
        )
        print(f"{file_name} 파일 카드가 나타남 확인")
    
    # 추가 안정화 대기
    time.sleep(3)  
    
    # 테스트 성공 여부 확인
    uploaded_image = driver.find_element(By.XPATH, f"//span[text()='{file_name}']")
    assert uploaded_image.is_displayed(), "업로드된 파일 카드가 화면에 나타나지 않았습니다."
    print("== 파일 업로드 완료 ==")
