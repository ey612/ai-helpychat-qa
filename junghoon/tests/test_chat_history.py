import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from junghoon.login import init_driver, login
from junghoon.chat_sendmessage import send_message
from junghoon.chat_history import ChatHistoryManager


@pytest.fixture(scope="function")
def driver():
    """
    - 브라우저/대기 객체 생성
    - 로그인
    - 히스토리 한 개 생성(메시지 전송)
    - 테스트 종료 후 브라우저 종료
    """
    driver, wait = init_driver()
    login(driver, wait)

    # 히스토리 하나를 만들기 위한 메시지 전송
    send_message(driver, "안녕하세요 자동화 테스트입니다. (히스토리 이름 변경용)")

    yield driver

    driver.quit()


def test_rename_history(driver):
    """
    채팅 히스토리 이름 변경 테스트
    1) old_text 로 히스토리 찾기
    2) new_text 로 이름 변경
    3) new_text 를 포함하는 히스토리 항목이 실제로 존재하는지 검증
    """
    history = ChatHistoryManager(driver)

    old_text = "안녕하세요 자동화 테스트입니다."
    new_text = "이름 변경 완료"

    # 1) 이름 변경 실행
    history.rename_history_and_save(old_text, new_text)

    # 2) 변경된 이름의 히스토리가 실제로 존재하는지 검증
    wait = WebDriverWait(driver, 10)
    histories = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "p.MuiTypography-root")
        )
    )

    matched = any(new_text in h.text for h in histories)

    assert matched, f"'{new_text}' 제목을 가진 히스토리 항목을 찾지 못했습니다."