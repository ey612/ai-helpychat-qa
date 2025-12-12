from pages.login_page import LoginPage
from pages.chat_page import ChatPage
from utils.constants import TEST_LOGIN_ID, TEST_LOGIN_PASSWORD


def test_chat_tc_001(driver):
    """채팅 문자열 전송 시 AI 응답 테스트"""
    login_page = LoginPage(driver)
    chat_page = ChatPage(driver)

    login_page.login(
        email=TEST_LOGIN_ID,
        password=TEST_LOGIN_PASSWORD,
    )

    chat_page.send_message(value="안녕하세요! 자동화 테스트 메시지입니다.")
    response = chat_page.check_ai_response()
    assert response is not None


def test_chat_tc_002(driver):
    """채팅 긴 문자열 전송 시 AI 응답 테스트"""
    login_page = LoginPage(driver)
    chat_page = ChatPage(driver)

    login_page.login(
        email=TEST_LOGIN_ID,
        password=TEST_LOGIN_PASSWORD,
    )

    chat_page.send_message(value="장문 문장 요약 입니다" * 1000)
    response = chat_page.check_ai_response()
    assert response is not None


def test_chat_tc_003(driver):
    """채팅 다시 생성 버튼 클릭 시 AI 응답 테스트"""
    login_page = LoginPage(driver)
    chat_page = ChatPage(driver)

    login_page.login(
        email=TEST_LOGIN_ID,
        password=TEST_LOGIN_PASSWORD,
    )

    chat_page.send_message(value="안녕하세요! 자동화 테스트 메시지입니다.")
    response = chat_page.check_ai_response()
    assert response is not None

    chat_page.click_regenerate_button()
    response = chat_page.check_ai_response()
    assert response is not None
