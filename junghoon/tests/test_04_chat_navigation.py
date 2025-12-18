import pytest
from selenium.webdriver.common.by import By

from junghoon.login import init_driver, login
from junghoon.chat_sendmessage import send_message
from junghoon.chat_regenerate import click_regenerate
from junghoon.chat_navigation import (
    click_prev_answer,
    click_next_answer,
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

    # 👉 이전/다음 답변 버튼이 보이도록,
    #    여기서 미리 메시지 전송 + 다시 생성까지 한 번 수행
    send_message(driver, "이전/다음 답변 테스트용 첫 질문입니다.")
    click_regenerate(driver, index=0)

    yield driver

    driver.quit()

def test_move_prev_then_next_answer(driver):
    """
    이전 답변으로 이동 후, 종료 없이 바로 다음 답변으로 이동 테스트
    """
    # 1) 이전 답변 이동
    click_prev_answer(driver)
    elements_prev = driver.find_elements(By.CSS_SELECTOR, AI_COMPLETE)
    assert len(elements_prev) > 0

    # 2) 같은 세션에서 바로 다음 답변 이동
    click_next_answer(driver)
    elements_next = driver.find_elements(By.CSS_SELECTOR, AI_COMPLETE)
    assert len(elements_next) > 0