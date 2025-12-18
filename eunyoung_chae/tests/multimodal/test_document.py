import time
import os
import pytest
from src.config.config import *
from src.utils.helpers import setup_driver, get_file_path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from src.pages.upload_page import UploadPage
from src.pages.login_page import LoginPage
from src.pages.main_page import GnbComponent

# [DOC_MDL_TC_001] 빈 문서가 정상 업로드되는지 확인

def test_001_document_upload_empty_file_succeeds(driver):
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 2. 문서 파일 경로 지정
    print("업로드 할 빈 문서 파일 경로")
    relative_path = '../../src/resources/asserts/files/test_empty.pdf'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path) 
    
    # 3. 문서 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)

    
    # 4. 문서 파일 업로드 확인
    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.presence_of_element_located((By.XPATH, f"//span[text()='{file_name}']"))
    )
    print("파일 카드가 나타남")
    
    # 추가 안정화 대기
    time.sleep(3)  
    
    # 테스트 성공 여부 확인
    uploaded_image = driver.find_element(By.XPATH, f"//span[text()='{file_name}']")
    assert uploaded_image.is_displayed(), "업로드된 빈 문서 파일 카드가 화면에 나타나지 않았습니다."
    print("== 빈 문서 파일 업로드 완료 ==")

# [DOC_MDL_TC_002] 암호화 문서 업로드 시 에러 메시지가 표시되는지 확인 

def test_002_document_upload_encrypted_file_shows_error(driver):
    
    # 1. 로그인
    login_page = LoginPage(driver) 
    login_page.login(PW, EMAIL)
    
    # 2. 문서 파일 경로 지정
    print("업로드 할 암호화 문서 파일 경로")
    relative_path = '../../src/resources/asserts/files/test_encrypted.docx'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path) 
    
    # 3. 문서 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)
    
    # 파일 첨부 성공 여부 확인 (파일 카드 생성이 나타나면 안 됨)
    try :
        
        print("파일 카드 생성 여부 확인 중")
        wait = WebDriverWait(driver, 10)
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
        
        assert "암호화" in alert_text, \
            f"예상과 다른 오류 메시지: {alert_text}"
            
        # if "암호화" in alert_text :
        #     print("테스트 통과: 암호화 안내 오류 메시지 확인됨")
        #     alert.accept()
        # else:
        #     alert.accept()
        #     pytest.fail(f"예상과 다른 오류 메시지: {alert_text}")
            
    except TimeoutException:
        print("테스트 실패: 오류 메시지가 나타나지 않음")
        pytest.fail("암호화 문서 파일 업로드 시 오류 메시지가 표시되지 않음")

#[DOC_MDL_TC_003] 지원 확장자 문서가 정상 업로드되는지 확인
@pytest.mark.parametrize(
    "file_name",
    [
        "test_normal.pdf",
        "test_normal.docx",
    ]
)
def test_003_document_upload_valid_extension_pdf(driver, file_name):
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 2. 문서 파일 경로 지정
    print(f"업로드 할 파일 경로: {file_name}")
    relative_path = f'../../src/resources/asserts/files/{file_name}'
    file_path = get_file_path(relative_path)

    # 3. 문서 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)
    
    # 4. 문서 파일 업로드 확인
    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.presence_of_element_located((By.XPATH, f"//span[text()='{file_name}']"))
    )
    print("파일 카드가 나타남")
    
    # 추가 안정화 대기
    time.sleep(3)  
    
    # 테스트 성공 여부 확인
    uploaded_image = driver.find_element(By.XPATH, f"//span[text()='{file_name}']")
    assert uploaded_image.is_displayed(), f"업로드된 {file_name} 파일 카드가 화면에 나타나지 않았습니다."
    print(f"== {file_name} 문서 파일 업로드 완료 ==")

# [DOC_MDL_TC_004] 미지원 확장자 문서 업로드 시 에러 메시지가 표시되는지 확인
@pytest.mark.parametrize(
    "file_name",
    [
        "test_fail.zip",
        "test_fail.exe",
        "test_fail.mp4",
    ]
)
def test_004_document_invalid_extensions_shows_error(driver, file_name) :
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 2. 문서 파일 경로 지정
    print(f"업로드 할 문서 파일 경로 {file_name}")
    relative_path = f'../../src/resources/asserts/files/{file_name}'
    file_path = get_file_path(relative_path)
    
    # 3. 문서 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)
    
    # 문서 파일 첨부 성공 여부 확인 (파일 카드 생성이 나타나면 안 됨)
    
    try :
        wait = WebDriverWait(driver, 10)
        print(f"{file_name} 파일 카드 생성 확인 중")
        wait.until(
            EC.presence_of_element_located((By.XPATH, f'//span[text()="{file_name}"]'))
        )
        pytest.fail(f"지원하지 않는 확장자 문서 파일({file_name}) 업로드 시 파일 카드가 표시되면 안 됩니다.")
        
    except TimeoutException:
        # 파일 카드가 나타나지 않으면 성공
        pass  
    
    # 업로드 실패 후 오류 메시지가 뜨는지 확인
    try:
        print("오류 메시지 확인 중")
        alert = wait.until(EC.alert_is_present())
        alert_text = alert.text
        print(f"Alert 메시지: {alert_text}")
        
        # "지원하지 않는" 문구가 포함되어 있는지 확인
        assert "지원하지 않는" in alert_text, \
                f"지원하지 않는 확장자 문서 파일 ({file_name}) 대한 오류 메시지가 표시되어야 합니다. (실제 메시지: {alert_text})"

        alert.accept()

    except TimeoutException:
        pytest.fail(
            f"지원하지 않는 확장자의 문서 파일({{file_name}}) 업로드 시 오류 메시지가 표시되어야 합니다."
        )
   
# [DOC_MDL_TC_005] 허용 용량 초과 문서 업로드 시 에러 메시지가 표시되는지 확인
@pytest.mark.parametrize(
    "file_name",
    [
        "test_50.1mb.pdf",
        "test_51mb.pdf",
        "test_60mb.pdf",
    ]
)
def test_005_document_upload_exceeds_max_size_shows_error(driver, file_name):
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 2. 문서 파일 경로 지정
    print(f"업로드 할 문서 파일 경로: {file_name}")
    relative_path = f'../../src/resources/asserts/files/{file_name}'
    file_path = get_file_path(relative_path)
    
    # 3. 문서 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)
    
    # 파일 첨부 성공 여부 확인 (파일 카드 생성이 나타나면 안 됨)
    try :
        print(f"({file_name})파일 카드 생성 여부 확인 중")
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.presence_of_element_located((By.XPATH, f"//span[text()='{file_name}']"))
        )
        pytest.fail(f"허용 용량 초과 문서 파일({file_name}) 업로드 시 파일 카드가 표시되면 안 됩니다.")
        
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
        
        assert "용량" in alert_text or "크기" in alert_text, \
            f"예상과 다른 오류 메시지: {alert_text}"
            
        print("테스트 통과: 허용 용량 초과 오류 메시지 확인됨")
        alert.accept()
            
    except TimeoutException:
        print("테스트 실패: 오류 메시지가 나타나지 않음")
        pytest.fail(f"허용 용량 초과 문서 파일({file_name}) 업로드 시 오류 메시지가 표시되지 않음")


    
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
    
    
    # 오류 메시지 확인 (오류 메시지가 노출 되어야 함)
    try:
        print("오류 메시지 확인 중")
        alert = wait.until(EC.alert_is_present())
        alert_text = alert.text
        print(f"Alert 메시지: {alert_text}")
        
        # "용량" 또는 "크기" 문구가 포함되어 있는지 확인
        assert "용량" in alert_text or "크기" in alert_text, \
            f"예상과 다른 오류 메시지: {alert_text}"
        print("테스트 통과: 허용 용량 초과 오류 메시지 확인됨")
        alert.accept()
            
    except TimeoutException:
        print("테스트 실패: 오류 메시지가 나타나지 않음")
        pytest.fail("허용 용량 초과 문서 파일 업로드 시 오류 메시지가 표시되지 않음")
   
# [DOC_MDL_TC_006] 경계값 용량 문서 업로드 시 정상 업로드되는지 확인 (49MB) / (49.9MB)
@pytest.mark.parametrize(
    "file_name",
    [
        "test_49mb.pdf",
        "test_49.9mb.docx",
    ]
)
def test_006_document_upload_boundary_size_succeeds(driver, file_name):
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 2. 문서 파일 경로 지정
    print(f"업로드 할 문서 파일 경로: {file_name}")
    relative_path = f'../../src/resources/asserts/files/{file_name}'
    file_path = get_file_path(relative_path)
    
    # 3. 문서 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)
    
    # 4. 문서 파일 업로드 확인
    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.presence_of_element_located((By.XPATH, f"//span[text()='{file_name}']"))
    )
    print("파일 카드가 나타남")
    
    # 추가 안정화 대기
    time.sleep(3)  
    
    # 테스트 성공 여부 확인
    uploaded_image = driver.find_element(By.XPATH, f"//span[text()='{file_name}']")
    assert uploaded_image.is_displayed(), f"업로드된 문서 ({file_name}) 파일 카드가 화면에 나타나지 않았습니다."
    print(f"== 문서 파일({file_name}) 업로드 완료 ==")

# [DOC_MDL_TC_007] 여러 문서 동시 업로드 시 정상 업로드되는지 확인

MULTI_DOC_FILES = [
        'test_multi_1.pdf',
        'test_multi_2.docx'
    ]
def test_007_document_upload_multiple_files_succeeds(driver):
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 파일 경로 지정
    file_names_to_upload = MULTI_DOC_FILES
    
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

    
    # 4. 문서 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_multiple_files(file_paths_list)
    time.sleep(5)
    print(f"== 다중 파일({file_name}) 업로드 요청 완료 ==")
    
    # 문서 파일 첨부 성공 여부 확인
    
    for file_name in file_names_to_upload:
        upload_document = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//span[text()='{file_name}']"))
        )
    # 테스트 성공 여부 확인
    assert upload_document.is_displayed(), f"업로드된({file_name}) 파일 카드가 화면에 나타나지 않았습니다."
    print(f"==({file_name}) 파일 업로드 완료 ==")

# [DOC_MDL_TC_008] 특수문자가 포함된 문서 파일명 업로드 시 정상 업로드 확인

def test_008_document_upload_filename_with_special_characters_succeeds(driver):
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 2. 문서 파일 경로 지정
    print("업로드 할 특수문자 포함된 파일명 문서 파일 경로")
    relative_path = '../../src/resources/asserts/files/test_한글@#$.pdf'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path) 
    
    # 3. 문서 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)

    # 4. 문서 파일 업로드 확인
    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.presence_of_element_located((By.XPATH, f"//span[text()='{file_name}']"))
    )
    print("파일 카드가 나타남")
    
    # 추가 안정화 대기
    time.sleep(3)  
    
    # 테스트 성공 여부 확인
    uploaded_image = driver.find_element(By.XPATH, f"//span[text()='{file_name}']")
    assert uploaded_image.is_displayed(), "업로드된 특수문자 포함된 파일명 문서 파일 카드가 화면에 나타나지 않았습니다."
    print(f"== 특수문자 포함된 파일명 문서 파일({file_name}) 업로드 완료 ==")

# [DOC_MDL_TC_009] 헤더가 손상된 문서 업로드 시 에러 메시지가 표시되는지 확인 

def test_009_document_upload_corrupted_header_shows_error(driver):
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 2. 문서 파일 경로 지정
    print("업로드 할 손상된 문서 파일 경로")
    relative_path = '../../src/resources/asserts/files/test_corrupted_invalid_header.pdf'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path) 
    
    # 3. 문서 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)
    
    
    # 파일 첨부 성공 여부 확인 (파일 카드 생성이 나타나면 안 됨)
    try :
        
        print(f"{file_name} 파일 카드 생성 여부 확인 중")
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.presence_of_element_located((By.XPATH, f"//span[text()='{file_name}']"))
        )
        pytest.fail(f"손상된 문서 파일({file_name}) 업로드 시 파일 카드가 표시되면 안 됩니다.")
        
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
        assert "손상" in alert_text or "잘못된 형식" in alert_text, \
            f"예상과 다른 오류 메시지: {alert_text}"
            
        print("테스트 통과: 손상된 파일 안내 오류 메시지 확인됨")
        alert.accept()

    except TimeoutException:
        print("테스트 실패: 오류 메시지가 나타나지 않음")
        pytest.fail("손상된 문서 파일 업로드 시 오류 메시지가 표시되지 않음")











