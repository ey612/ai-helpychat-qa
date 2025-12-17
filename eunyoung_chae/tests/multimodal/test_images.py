import time
import os
import pytest
from src.config.config import *
from src.utils.helpers import login, setup_driver, logout, get_file_path, open_file_upload_dialog
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


# [IMG_MDL_TC_001] 지원 확장자 이미지가 정상 업로드되는지 확인

def test_001_image_upload_valid_extension_jpg():
    
    # 1. 로그인, driver 객체
    driver = setup_driver(EMAIL, PW)
    wait = WebDriverWait(driver, 10)
    
    # 2. 이미지 파일 업로드 하기
    open_file_upload_dialog(driver)
    
    # 3. 이미지 파일 경로 지정
    print("업로드 할 JPG 이미지 파일 경로")
    relative_path = '../../src/resources/asserts/images/test_normal.jpg'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path)

    
    # 4. 이미지 파일 업로드
    print("JPG 이미지 파일 업로드 시도 중")
    file_input_element = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    file_input_element.send_keys(file_path)
    time.sleep(5)
    
    # 5. 업로드 확인
    print("JPG 이미지 파일 미리보기 확인 중")
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f'img[alt="{file_name}"]'))
    )
    print("JPG 이미지 파일 미리보기 나타남")
    
    # 추가 안정화 대기
    time.sleep(3)  
    
    # 테스트 성공 여부 확인
    uploaded_image = driver.find_element(By.CSS_SELECTOR, f'img[alt="{file_name}"]')
    assert uploaded_image.is_displayed(), "업로드된 JPG 이미지 파일 미리보기가 화면에 나타나지 않았습니다."
    print("== JPG 이미지 파일 업로드 완료 ==")
    
def test_001_image_upload_valid_extension_png():
     # 1. 로그인, driver 객체
    driver = setup_driver(EMAIL, PW)
    wait = WebDriverWait(driver, 10)
    
    # 2. 이미지 파일 업로드 하기
    open_file_upload_dialog(driver)
    
    # 3. 이미지 파일 경로 지정
    print("업로드 할 PNG 이미지 경로")
    relative_path = '../../src/resources/asserts/images/test_normal.png'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path)

    # 4. 이미지 파일 업로드
    print("PNG 이미지 파일 업로드 시도 중")
    file_input_element = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    file_input_element.send_keys(file_path)
    time.sleep(5)
    
    # 5. 업로드 확인
    print("PNG 이미지 파일 미리보기 확인 중")
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f'img[alt="{file_name}"]'))
    )
    print("PNG 이미지 파일 미리보기 나타남")
    
    # 추가 안정화 대기
    time.sleep(3)  
    
    # 테스트 성공 여부 확인
    uploaded_image = driver.find_element(By.CSS_SELECTOR, f'img[alt="{file_name}"]')
    assert uploaded_image.is_displayed(), "업로드된 PNG 이미지 파일 미리보기가 화면에 나타나지 않았습니다."
    print("== PNG 이미지 파일 업로드 완료 ==")

# [IMG_MDL_TC_002] 미지원 확장자 이미지 업로드 시 에러 메시지가 표시되는지 확인

def test_002_image_invalid_extensions_shows_error_svg() :
    
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
        
def test_002_image_invalid_extensions_shows_error_ico() :
    
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

# [IMG_MDL_TC_003] 허용 용량 초과 이미지 업로드 시 에러 메시지가 표시되는지 확인    

def test_003_image_upload_exceeds_max_size_shows_error_50mb():
    
    # 1. 로그인, driver 객체
    driver = setup_driver(EMAIL, PW)
    wait = WebDriverWait(driver, 10)
    
    # 2. 이미지 파일 업로드 하기
    open_file_upload_dialog(driver)
    
    # 3. 이미지 파일 경로 지정
    print("업로드 할 50MB 이미지 파일 경로")
    relative_path = '../../src/resources/asserts/files/test_50mb.pdf'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path) 
    
     # 4. 이미지 파일 업로드
    print("50MB 이미지 파일 업로드 중")
    file_input_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    file_input_element.send_keys(file_path)
    time.sleep(3)
    
    # 이미지 파일 첨부 성공 여부 확인 (미리보기가 나타나면 안 됨)
    try :
        print("50MB 이미지 파일 미리보기 확인 중")
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'img[alt="{file_name}"]'))
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
            
    except TimeoutException:
        print("테스트 실패: 오류 메시지가 나타나지 않음")
        pytest.fail("허용 용량 초과 이미지 파일 업로드 시 오류 메시지가 표시되지 않음")
        
def test_003_image_upload_exceeds_max_size_shows_error_50_1mb():
    
    # 1. 로그인, driver 객체
    driver = setup_driver(EMAIL, PW)
    wait = WebDriverWait(driver, 10)
    
    # 2. 이미지 파일 업로드 하기
    open_file_upload_dialog(driver)
    
    # 3. 이미지 파일 경로 지정
    print("업로드 할 50MB 이미지 파일 경로")
    relative_path = '../../src/resources/asserts/files/test_50.1mb.pdf'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path) 
    
     # 4. 이미지 파일 업로드
    print("50MB 이미지 파일 업로드 중")
    file_input_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    file_input_element.send_keys(file_path)
    time.sleep(3)
    
    # 이미지 파일 첨부 성공 여부 확인 (미리보기가 나타나면 안 됨)
    try :
        print("50MB 이미지 파일 미리보기 확인 중")
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'img[alt="{file_name}"]'))
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

            
    except TimeoutException:
        print("테스트 실패: 오류 메시지가 나타나지 않음")
        pytest.fail("허용 용량 초과 이미지 파일 업로드 시 오류 메시지가 표시되지 않음")

def test_003_image_upload_exceeds_max_size_shows_error_51mb():
    
    # 1. 로그인, driver 객체
    driver = setup_driver(EMAIL, PW)
    wait = WebDriverWait(driver, 10)
    
    # 2. 이미지 파일 업로드 하기
    open_file_upload_dialog(driver)
    
    # 3. 이미지 파일 경로 지정
    print("업로드 할 51MB 이미지 파일 경로")
    relative_path = '../../src/resources/asserts/files/test_51mb.pdf'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path) 
    
     # 4. 이미지 파일 업로드
    print("51MB 이미지 파일 업로드 중")
    file_input_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    file_input_element.send_keys(file_path)
    time.sleep(3)
    
    # 이미지 파일 첨부 성공 여부 확인 (미리보기가 나타나면 안 됨)
    try :
        print("51MB 이미지 파일 미리보기 확인 중")
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'img[alt="{file_name}"]'))
        )
        pytest.fail("허용 용량 초과 이미지 파일 업로드 시 미리보기가 표시되면 안 됩니다.")
    
    except TimeoutException:
        # 미리보기가 나타나지 않으면 성공
        pass
    
    
     # 오류 메시지 확인
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
        pytest.fail("허용 용량 초과 이미지 파일 업로드 시 오류 메시지가 표시되지 않음")   
        
def test_003_image_upload_exceeds_max_size_shows_error_60mb():
     # 1. 로그인, driver 객체
    driver = setup_driver(EMAIL, PW)
    wait = WebDriverWait(driver, 10)
    
    # 2. 이미지 파일 업로드 하기
    open_file_upload_dialog(driver)
    
    # 3. 이미지 파일 경로 지정
    print("업로드 할 60MB 이미지 파일 경로")
    relative_path = '../../src/resources/asserts/files/test_60mb.pdf'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path) 
    
     # 4. 이미지 파일 업로드
    print("60MB 이미지 파일 업로드 중")
    file_input_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    file_input_element.send_keys(file_path)
    time.sleep(3)
    
    # 이미지 파일 첨부 성공 여부 확인 (미리보기가 나타나면 안 됨)
    try :
        print("60MB 이미지 파일 미리보기 확인 중")
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'img[alt="{file_name}"]'))
        )
        pytest.fail("허용 용량 초과 이미지 파일 업로드 시 미리보기가 표시되면 안 됩니다.")
    
    except TimeoutException:
        # 미리보기가 나타나지 않으면 성공
        pass
    
    
     # 오류 메시지 확인
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
        pytest.fail("허용 용량 초과 이미지 파일 업로드 시 오류 메시지가 표시되지 않음")   
        

# [IMG_MDL_TC_004] 경계값 용량 이미지 업로드 시 정상 업로드되는지 확인 (49MB) / (49.9MB)

def test_004_image_upload_boundary_size_49mb_succeeds():
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

def test_004_image_upload_boundary_size_49_9mb_succeeds():
    
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

# [IMG_MDL_TC_005] 여러 이미지 동시 업로드 시 정상 업로드되는지 확인

def test_005_image_upload_multiple_files() :
     
     # 1. 로그인, driver 객체
    driver = setup_driver(EMAIL, PW)
    wait = WebDriverWait(driver, 10)
    
    # 2. 이미지 파일 업로드 하기
    open_file_upload_dialog(driver)
    
    #  3. 이미지 파일 경로 지정
    
    print("업로드 할 이미지 파일 목록 만들기")
    file_names_to_upload = [
        
        'test_multi_1.jpg',
        'test_multi_2.png'
    ]
    
    # current_dir
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_paths_list = []
    
    # 최종 경로 합치기
    print("업로드 할 이미지 파일 경로 찾기")
    for file_name in file_names_to_upload:
        
        # 상대 경로 설정
        relative_path = f'../../src/resources/asserts/images/{file_name}'

       # 최종 이미지 경로 (컴퓨터는 이 경로를 보고 찾아 감) 
        combined_path = os.path.join(current_dir, relative_path)
        file_path = os.path.abspath(combined_path)
        print(f"계산된 파일 경로: {file_path}")

    
        # 파일 존재 여부 확인
        print("이미지 파일이 존재 하는지 확인하는 중")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
        
        # 파일 경로를 리스트에 추가
        file_paths_list.append(file_path)
    
    files_to_send = '\n'.join(file_paths_list)
    print(f"Selenium에 전송할 문자열:\n{files_to_send}")
    
    # 4. 이미지 파일 업로드
    file_input_element = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    file_input_element.send_keys(files_to_send)
    time.sleep(5)
    print("== 다중 파일 업로드 요청 완료 ==")
    
    # 이미지 파일 첨부 성공 여부 확인
    
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

# [IMG_MDL_TC_006] 특수문자가 포함된 이미지 파일명 업로드 시 정상 업로드 확인

def test_006_image_upload_filename_with_special_characters_succeeds():
    
    # 1. 로그인, driver 객체
    driver = setup_driver(EMAIL, PW)
    wait = WebDriverWait(driver, 10)
    
    # 2. 이미지 파일 업로드 하기
    open_file_upload_dialog(driver)
    
    # 3. 이미지 파일 경로 지정
    print("업로드 할 특수문자 포함된 파일명 이미지 파일 경로")
    relative_path = '../../src/resources/asserts/images/test_한글@#$.jpg'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path)

    
    # 4. 이미지 파일 업로드
    print("특수문자 포함된 파일명 이미지 파일 업로드 시도 중")
    file_input_element = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    file_input_element.send_keys(file_path)
    time.sleep(5)
    
    # 5. 업로드 확인
    print("특수문자 포함된 파일명 이미지 파일 미리보기 확인 중")
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f'img[alt="{file_name}"]'))
    )
    print("특수문자 포함된 파일명 이미지 파일 미리보기 나타남")
    
    # 추가 안정화 대기
    time.sleep(3)  
    
    # 테스트 성공 여부 확인
    uploaded_image = driver.find_element(By.CSS_SELECTOR, f'img[alt="{file_name}"]')
    assert uploaded_image.is_displayed(), "업로드된 특수문자 포함된 파일명 이미지 파일 미리보기가 화면에 나타나지 않았습니다."
    print("== 특수문자 포함된 파일명 이미지 파일 업로드 완료 ==")

# [IMG_MDL_TC_007] 헤더가 손상된 이미지 업로드 시 에러 메시지가 표시되는지 확인

def test_007_image_upload_corrupted_header_shows_error():
    
    # 1. 로그인, driver 객체
    driver = setup_driver(EMAIL, PW)
    wait = WebDriverWait(driver, 10)
    
    # 2. 이미지 파일 업로드 하기
    open_file_upload_dialog(driver)
    
    # 3. 이미지 파일 경로 지정
    print("업로드 할 손상된 이미지 파일 경로")
    relative_path = '../../src/resources/asserts/images/test_corrupted_invalid_header.jpg'
    file_path = get_file_path(relative_path)
    file_name = os.path.basename(file_path) 
    
     # 4. 이미지 파일 업로드
    print("손상된 이미지 파일 업로드 중")
    file_input_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    file_input_element.send_keys(file_path)
    time.sleep(3)
    
    # 이미지 파일 첨부 성공 여부 확인 (미리보기가 나타나면 안 됨)
    try :
        print("손상된 이미지 파일 미리보기 확인 중")
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'img[alt="{file_name}"]'))
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
        
    except TimeoutException:
        print("테스트 실패: 오류 메시지가 나타나지 않음")
        pytest.fail("손상된 이미지 파일 업로드 시 오류 메시지가 표시되지 않음")
