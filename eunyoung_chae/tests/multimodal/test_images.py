import os
import time
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from src.pages.upload_page import UploadPage
from src.pages.login_page import LoginPage
from src.config.config import EMAIL, PW
from src.utils.helpers import get_file_path

# [IMG_MDL_TC_001] 지원 확장자 이미지가 정상 업로드되는지 확인

@pytest.mark.parametrize(
    "file_name",
    [
        "test_normal.jpg",
        "test_normal.png",
    ]
)
def test_001_image_upload_valid_extension(driver, file_name):
    wait = WebDriverWait(driver, 10)
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 2. 이미지 파일 경로 설정
    print(f"업로드 할 이미지 파일 경로{file_name}")
    relative_path = f'../../src/resources/asserts/images/{file_name}'
    file_path = get_file_path(relative_path)
    
    # 3. 이미지 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)
    
    # 4. 업로드 확인
    print(f"{file_name} 이미지 파일 미리보기 확인 중")
    
    uploaded_image = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f'img[alt="{file_name}"]'))
    )
    print(f"{file_name} 이미지 파일 미리보기 나타남")
    
    # 테스트 성공 여부 확인
    assert uploaded_image.is_displayed(), f"업로드된 이미지 파일 {file_name} 미리보기가 화면에 나타나지 않았습니다."
    print(f"== {file_name} 이미지 파일 업로드 완료 ==")

# [IMG_MDL_TC_002] 미지원 확장자 이미지 업로드 시 에러 메시지가 표시되는지 확인

@pytest.mark.parametrize(
    "file_name",
    [
        "test_fail.svg",
        "test_fail.ico",
        
    ]
)
def test_002_image_invalid_extensions_shows_error(driver, file_name) :
    wait = WebDriverWait(driver, 10)
    
     # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 2. 이미지 파일 경로 지정
    print(f"업로드 할 이미지 파일 경로{file_name}")
    relative_path = f'../../src/resources/asserts/images/{file_name}'
    file_path = get_file_path(relative_path)
    
    # 3. 이미지 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)
    
    # 이미지 파일 첨부 성공 여부 확인 (미리보기가 나타나면 안 됨)
    
    try :        
        print(f"{file_name} 이미지 파일 미리보기 확인 중")
        wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, f'img[alt="{file_name}"]'))
        )
        pytest.fail(f"지원하지 않는 확장자 {file_name} 이미지 파일 업로드 시 미리보기가 표시되면 안 됩니다.")
        
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
        print("미지원 확장자 이미지 업로드 오류 메시지 확인 완료")

    except TimeoutException:
        pytest.fail(
            "지원하지 않는 확장자[.SVG]의 이미지 파일 업로드 시 오류 메시지가 표시되어야 합니다."
        )

# [IMG_MDL_TC_003] 허용 용량 초과 이미지 업로드 시 에러 메시지가 표시되는지 확인    

@pytest.mark.parametrize(
    "file_name",
    [
        "test_50.1mb.pdf",
        "test_51mb.pdf",
        "test_60mb.pdf",
    ]
)
def test_003_image_upload_exceeds_max_size_shows_error(driver, file_name):
    wait = WebDriverWait(driver, 10)
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    
    # 2. 이미지 파일 경로 지정
    print(f"업로드 할 {file_name} 이미지 파일 경로")
    relative_path = f'../../src/resources/asserts/files/{file_name}'
    file_path = get_file_path(relative_path)
    
     # 3. 이미지 파일 업로드
    print(f"{file_name} 이미지 파일 업로드 중")
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)
    
    # 이미지 파일 첨부 성공 여부 확인 (미리보기가 나타나면 안 됨)
    try :
        print(f"{file_name} 이미지 파일 미리보기 확인 중")
        wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, f'img[alt="{file_name}"]'))
        )
        pytest.fail("허용 용량 초과 이미지 파일 업로드 시 미리보기가 표시되면 안 됩니다.")
    
    except TimeoutException:
        # 미리보기가 나타나지 않으면 성공
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
        print("허용 용량 초과 이미지 업로드 오류 메시지 확인 완료")

    except TimeoutException:
        print("테스트 실패: 오류 메시지가 나타나지 않음")
        pytest.fail("허용 용량 초과 이미지 파일 업로드 시 오류 메시지가 표시되지 않음")

# [IMG_MDL_TC_004] 경계값 용량 이미지 업로드 시 정상 업로드되는지 확인 (49MB) / (49.9MB)

@pytest.mark.parametrize(
    "file_name",
    [
        "test_49mb.jpg",
        "test_49.9mb.jpg",
    ]
)
def test_004_image_upload_boundary_size_succeeds(driver, file_name):
    wait = WebDriverWait(driver, 10)
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 2. 이미지 파일 경로 지정
    print(f"업로드 할 {file_name} 이미지 파일 경로")
    relative_path = f'../../src/resources/asserts/images/{file_name}'
    file_path = get_file_path(relative_path)
    
    # 3. 이미지 파일 업로드 하기
    print(f"{file_name} 이미지 파일 업로드 시도 중")
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)
    
    # 4. 업로드 확인
    print(f"{file_name} 이미지 파일 미리보기 확인 중")
    uploaded_image = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f'img[alt="{file_name}"]'))
    )
    print(f"{file_name} 이미지 파일 미리보기 나타남")
    
    # 테스트 성공 여부 확인
    assert uploaded_image.is_displayed(), "업로드된 49MB 이미지 파일 미리보기가 화면에 나타나지 않았습니다."
    print(f"== {file_name} 이미지 파일 업로드 완료 ==")

# [IMG_MDL_TC_005] 여러 이미지 동시 업로드 시 정상 업로드되는지 확인

MULTI_IMAGE_FILES = [
    
    'test_multi_1.jpg',
    'test_multi_2.png'
]
def test_005_image_upload_multiple_files(driver) :
    
     # 1. 로그인
    
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    
    file_paths = [
        
        get_file_path(f'../../src/resources/asserts/images/{file_name}')
        for file_name in MULTI_IMAGE_FILES
    ]
    
    upload_page.upload_multiple_files(file_paths)

    for file_name in MULTI_IMAGE_FILES:
        upload_image = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, f'img[alt="{file_name}"]'))
        )
        assert upload_image.is_displayed(), "업로드된 파일 미리보기 이미지가 화면에 나타나지 않았습니다."
        print("== 파일 업로드 완료 ==")

# [IMG_MDL_TC_006] 특수문자가 포함된 이미지 파일명 업로드 시 정상 업로드 확인

def test_006_image_upload_filename_with_special_characters_succeeds(driver):
    wait = WebDriverWait(driver, 10)
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 3. 이미지 파일 경로 지정
    print("업로드 할 특수문자 포함된 파일명 이미지 파일 경로")
    relative_path = '../../src/resources/asserts/images/test_한글@#$.jpg'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path)

    # 4. 이미지 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)
    
    # 4. 업로드 확인
    print("특수문자 포함된 파일명 이미지 파일 미리보기 확인 중")
    
    uploaded_image = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f'img[alt="{file_name}"]'))
    )
    print("특수문자 포함된 파일명 이미지 파일 미리보기 나타남") 
    
    # 테스트 성공 여부 확인
    assert uploaded_image.is_displayed(), "업로드된 특수문자 포함된 파일명 이미지 파일 미리보기가 화면에 나타나지 않았습니다."
    print("== 특수문자 포함된 파일명 이미지 파일 업로드 완료 ==")

# [IMG_MDL_TC_007] 헤더가 손상된 이미지 업로드 시 에러 메시지가 표시되는지 확인

def test_007_image_upload_corrupted_header_shows_error(driver):
    wait = WebDriverWait(driver, 10)
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)
    
    # 2. 이미지 파일 경로 지정
    print("업로드 할 손상된 이미지 파일 경로")
    relative_path = '../../src/resources/asserts/images/test_corrupted_invalid_header.jpg'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path) 
    
    # 3. 이미지 파일 업로드
    upload_page = UploadPage(driver)
    upload_page.open_file_upload_dialog()
    upload_page.upload_file(file_path)
    
    # 이미지 파일 첨부 성공 여부 확인 (미리보기가 나타나면 안 됨)
    try :
        print("손상된 이미지 파일 미리보기 확인 중")
        
        wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, f'img[alt="{file_name}"]'))
        )
        pytest.fail("손상된 이미지 파일 업로드 시 미리보기가 표시되면 안 됩니다.")
    
    except TimeoutException:
        # 미리보기가 나타나지 않으면 성공
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
            
        print("테스트 통과: 손상되었거나 잘못된 형식을 안내하는 오류 메시지 확인됨")
        alert.accept()
        print("손상된 이미지 업로드 오류 메시지 확인 완료")
        
    except TimeoutException:
        print("테스트 실패: 오류 메시지가 나타나지 않음")
        pytest.fail("손상된 이미지 파일 업로드 시 오류 메시지가 표시되지 않음")
