# tests/test_login.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from junghoon.login import init_driver, login


def test_login_success():
    # 1) 드라이버/대기 객체 초기화
    driver, wait = init_driver()

    try:
        # 2) 로그인 수행
        login(driver, wait)

        # 3) 로그인 성공 여부 검증
        #    - 예: 로그인 후 특정 요소(예: 사용자 이름, 로그아웃 버튼 등)가 보이는지 체크
        #    - 여기서는 예시로, 로그인 후 URL이 바뀌거나, 특정 텍스트가 보이는지 확인할 수 있음

        # (예시 1) URL이 로그인 페이지가 아닌지 확인
        time.sleep(2)  # 페이지 전환 대기(필요 시)
        current_url = driver.current_url
        assert "login" not in current_url.lower()

        # (예시 2) 로그인 후 헤더나 버튼 요소 체크 (실제 화면에 맞게 수정 필요)
        # 예: 로그아웃 버튼이 뜨는지 확인
        logout_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='button']"))
        )
        assert logout_button is not None

    finally:
        # 4) 테스트 끝나면 브라우저 닫기
        driver.quit()