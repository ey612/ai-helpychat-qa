import pytest
from selenium.webdriver.common.by import By

from junghoon.login import init_driver, login
from junghoon.chat_sendmessage import send_message
from junghoon.chat_editmessage import (
    click_edit_button,
    edit_textarea_message,
)
from junghoon.constants import AI_COMPLETE


@pytest.fixture(scope="function")
def driver():
    """
    - 브라우저/대기 객체 생성
    - 로그인
    - 테스트 종료 후 브라우저 종료
    """
    driver, wait = init_driver()
    login(driver, wait)

    # 수정 테스트를 위해, 먼저 원본 메시지 하나 보냄
    send_message(driver, "수정 전 메시지입니다.")

    yield driver

    driver.quit()


def test_edit_last_message(driver):
    """
    마지막 질문을 수정하고, 수정 후에도 AI 응답이 정상적으로 도착하는지 테스트
    """

    # 1) 마지막 메시지에 마우스 오버 후 '수정' 버튼 클릭
    click_edit_button(driver)

    # 2) 수정 텍스트 입력 후 엔터 (재실행)
    new_text = "수정 후 메시지 입니다."
    edit_textarea_message(driver, new_text)

    # 3) 검증: AI_COMPLETE 기준 요소가 다시 존재하는지 확인
    elements = driver.find_elements(By.CSS_SELECTOR, AI_COMPLETE)
    assert len(elements) > 0