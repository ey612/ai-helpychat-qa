import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait

from junghoon.login import init_driver, login
from junghoon.logout import logout


@pytest.fixture(scope="function")
def driver():
    driver, wait = init_driver()
    login(driver, wait)
    yield driver
    # driver.quit()  # 창 안 닫고 유지하고 싶으면 주석 유지


def test_logout(driver):
    """
    로그아웃 테스트
    - 로그아웃 버튼 클릭
    - 로그인 페이지로 이동했는지 검증
    - 뒤로 가기 여러 번 클릭 시에도 로그인 페이지 유지 확인
    """
    logout(driver)
    wait = WebDriverWait(driver, 10)

    # then 1: 로그인 페이지 이동 확인
    wait.until(lambda d: "signin" in d.current_url.lower() or "login" in d.current_url.lower())
    url_after_logout = driver.current_url.lower()
    print("🔹 after logout:", url_after_logout)
    assert "signin" in url_after_logout or "login" in url_after_logout

    # when: 뒤로 가기 여러 번
    back_times = 3  # 🔹 원하는 횟수로 바꿔도 됨
    for i in range(back_times):
        driver.back()
        print(f"뒤로가기 버튼 클릭 {i+1}회")
        time.sleep(1)  # 너무 빠르게 안 보내고 1초씩 텀 주기 (선택)

    # then 2: 여러 번 뒤로 가기 후에도 로그인 페이지 유지
    wait.until(lambda d: "signin" in d.current_url.lower() or "login" in d.current_url.lower())
    url_after_back = driver.current_url.lower()
    print("🔹 after multi back:", url_after_back)
    assert "signin" in url_after_back or "login" in url_after_back

    # 디버깅용으로 화면 보고 싶으면
    time.sleep(2)