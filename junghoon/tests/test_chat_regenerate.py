import pytest
from junghoon.login import init_driver, login
from junghoon.chat_sendmessage import send_message
from junghoon.chat_regenerate import click_regenerate

def test_click_regenerate():
    driver, wait = init_driver()

    try:
        # 로그인
        login(driver, wait)

        # 질문 전송
        send_message(driver, "다시 생성 테스트입니다.")

        # 다시 생성 클릭 (첫 번째 버튼)
        click_regenerate(driver, index=0)

        # 여기까지 왔으면 성공
        assert True

    finally:
        # ❗ 테스트 끝나도 브라우저 유지하고 싶으면 주석
        # driver.quit()
        pass