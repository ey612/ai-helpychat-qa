import time
import os
from src.config.config import *
from src.utils.helpers import login, setup_driver, logout, get_file_path, open_file_upload_dialog
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


# [DOC_MDL_TC_001] 지원 확장자 문서가 정상 업로드되는지 확인

def test_document_upload_valid_extension_pdf():
    
    # 1. 로그인, driver 객체
    driver = setup_driver(EMAIL, PW)
    wait = WebDriverWait(driver, 10)
    
    # 2. 파일 업로드 창 열기
    open_file_upload_dialog(driver)
    
    # 3. 문서 파일 경로 지정
    print("업로드 할 PDF 파일 경로")
    relative_path = '../../src/resources/asserts/files/test_normal.pdf'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path) 
    
    # 4. 문서 파일 업로드
    print("PDF 파일 업로드 시도 중")
    file_input_element = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    file_input_element.send_keys(file_path)
    time.sleep(5)
    
    # 5. 문서 업로드 확인
    wait.until(
        EC.presence_of_element_located((By.XPATH, f"//span[text()='{file_name}']"))
    )
    print("파일 카드가 나타남")
    
    # 추가 안정화 대기
    time.sleep(3)  
    
    # 테스트 성공 여부 확인
    uploaded_image = driver.find_element(By.XPATH, f"//span[text()='{file_name}']")
    assert uploaded_image.is_displayed(), "업로드된 PDF 파일 카드가 화면에 나타나지 않았습니다."
    print("== PDF파일 업로드 완료 ==")
    
def test_document_upload_valid_extension_doc():
    
    # 1. 로그인, driver 객체
    driver = setup_driver(EMAIL, PW)
    wait = WebDriverWait(driver, 10)
    
    # 2. [파일 업로드] 열기
    open_file_upload_dialog(driver)
    
    # 3. 문서 파일 경로 지정
    print("업로드 할 DOC 파일 경로")
    relative_path = '../../src/resources/asserts/files/test_normal.doc'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path) 
    
    # 4. 문서 파일 업로드
    print("DOC 파일 업로드 시도 중")
    file_input_element = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    #file_input_element = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
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
    assert uploaded_image.is_displayed(), "업로드된 DOC 파일 카드가 화면에 나타나지 않았습니다."
    print("== 파일 업로드 완료 ==")
    
def test_document_upload_valid_extension_xlsx():
    
    # 1. 로그인, driver 객체
    driver = setup_driver(EMAIL, PW)
    wait = WebDriverWait(driver, 10)
    
    # 2. [파일 업로드] 열기
    open_file_upload_dialog(driver)
    
    # 3. 문서 파일 경로 지정
    print("업로드 할 XLSX 파일 경로")
    relative_path = '../../src/resources/asserts/files/test_normal.xlsx'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path) 
    
    # 4. 문서 파일 업로드
    print("XLSX 파일 업로드 시도 중")
    file_input_element = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    #file_input_element = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
    file_input_element.send_keys(file_path)
    time.sleep(5)
    
    # 5. 문서 업로드 확인
    
    wait.until(
        EC.presence_of_element_located((By.XPATH, f"//span[text()='{file_name}']"))
    )
    print("파일 카드가 나타남")
    
    # 추가 안정화 대기
    time.sleep(3)  
    
    # 테스트 성공 여부 확인
    uploaded_image = driver.find_element(By.XPATH, f"//span[text()='{file_name}']")
    assert uploaded_image.is_displayed(), "업로드된 XLSX 파일 카드가 화면에 나타나지 않았습니다."
    print("== 파일 업로드 완료 ==")
    
def test_document_upload_valid_extension_txt():
    
    # 1. 로그인, driver 객체
    driver = setup_driver(EMAIL, PW)
    wait = WebDriverWait(driver, 10)
    
    # 2. [파일 업로드] 열기
    open_file_upload_dialog(driver)
    
    # 3. 문서 파일 경로 지정
    print("업로드 할 TXT 파일 경로")
    relative_path = '../../src/resources/asserts/files/test_normal.txt'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path) 
    
    # 4. 문서 파일 업로드
    print("TXT 파일 업로드 시도 중")
    file_input_element = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    #file_input_element = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
    file_input_element.send_keys(file_path)
    time.sleep(5)
    
    # 5. 문서 업로드 확인
    
    wait.until(
        EC.presence_of_element_located((By.XPATH, f"//span[text()='{file_name}']"))
    )
    print("파일 카드가 나타남")
    
    # 추가 안정화 대기
    time.sleep(3)  
    
    # 테스트 성공 여부 확인
    uploaded_image = driver.find_element(By.XPATH, f"//span[text()='{file_name}']")
    assert uploaded_image.is_displayed(), "업로드된 TXT 파일 카드가 화면에 나타나지 않았습니다."
    print("== 파일 업로드 완료 ==")
