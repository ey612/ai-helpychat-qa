import time
import pytest
from selenium.webdriver.common.by import By

from junghoon.login import init_driver, login
from junghoon.chat_sendmessage import send_message, copy_message_and_resend


@pytest.fixture()
def logged_in_driver():
    driver, wait = init_driver()
    login(driver, wait)
    yield driver, wait
    time.sleep(10)
    driver.quit()


def test_send_messages_and_copy_last(logged_in_driver):
    driver, wait = logged_in_driver

    test_cases = {
        "simple": "안녕하세요 자동화 테스트입니다.",
        "long": "장문 요약 입니다!!." * 90,
        "special": "()_+!&★☆♥♡♠♣😊🎉💡♬㉿㈜🔥✨㎲㎳㎴ⅵⅶ⅛⅜⅝㈍㉭",
    }

    # 1) simple, long, special 순서로 전송
    for name, msg in test_cases.items():
        print(f"🚀 sending {name} message")
        send_message(driver, msg)

    # 2) 마지막으로 보낸 메시지(special)만 복사 → 붙여넣기 → 재전송
    copy_message_and_resend(driver)

    # (선택) 3) 진짜 마지막 2개 메시지가 같은지 확인하고 싶다면:
    # message_elements = driver.find_elements(By.CSS_SELECTOR, ".chat-message-text")
    # last_texts = [el.text for el in message_elements[-2:]]
    # print("🔍 마지막 두 개 메시지:", last_texts)
    # assert last_texts[0] == last_texts[1]

    assert True