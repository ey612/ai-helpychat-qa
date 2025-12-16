import pytest
from junghoon.login import init_driver, login
from junghoon.chat_sendmessage import send_message
from junghoon.constants import AI_COMPLETE

@pytest.fixture
def logged_in_driver():
    # 1) 브라우저 실행 + 기본 페이지 진입
    driver, wait = init_driver()

    # 2) 로그인 수행
    login(driver, wait)

    # 3) 테스트에 driver/wait 넘겨주기
    yield driver, wait

    # 4) 테스트 끝나면 브라우저 닫기
    driver.quit()

def test_send_message_simple(logged_in_driver):
    driver, wait = logged_in_driver

    # 1) 짧은 메시지 전송
    send_message(driver, "안녕하세요 자동화 테스트입니다.")

    # 2) 아주 간단한 검증: 에러 없이 여기까지 오면 일단 PASS
    #    - 나중에는 채팅 목록/메시지 버블이 실제로 생겼는지까지 체크 가능
    assert True

def test_send_message_long(logged_in_driver):
    driver, wait = logged_in_driver

    # 1) 긴 메시지 전송
    long_msg = "장문 요약 입니다!!." * 90
    send_message(driver, long_msg)

    # 2) 마찬가지로 에러 없이 완료되면 PASS
    assert True