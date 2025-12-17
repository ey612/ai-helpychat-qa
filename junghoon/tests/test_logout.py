import pytest
from selenium.webdriver.support.ui import WebDriverWait

from junghoon.login import init_driver, login
from junghoon.logout import logout


@pytest.fixture(scope="function")
def driver():
    driver, wait = init_driver()
    login(driver, wait)
    yield driver
    driver.quit()


def test_logout(driver):
    """
    로그아웃 테스트
    - 로그아웃 버튼 클릭
    - 로그인 페이지로 이동했는지 검증
    """

    # when
    logout(driver)
    wait = WebDriverWait(driver, 10)

    # then
    wait.until(lambda d: "signin" in d.current_url.lower() or "login" in d.current_url.lower())
    current_url = driver.current_url.lower()
    assert "signin" in current_url or "login" in current_url