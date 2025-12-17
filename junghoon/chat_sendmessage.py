from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from junghoon.constants import AI_COMPLETE

# ChromeDriver 가 BMP(0xFFFF 이하)만 지원하는 환경이므로 True 유지
CHROMEDRIVER_BMP_ONLY = True


def _to_bmp_only(text: str) -> str:
    """ChromeDriver가 지원하지 않는 비-BMP 문자(대부분 이모지)를 제거."""
    return "".join(c for c in text if ord(c) <= 0xFFFF)


def send_message(driver, message: str, timeout: int = 30):
    """
    1) (필요 시) 비-BMP 문자 제거
    2) textarea에 메시지 입력
    3) aria-label="보내기" 버튼 클릭으로 전송
    4) AI_COMPLETE 요소가 나타날 때까지 대기
    """
    wait = WebDriverWait(driver, timeout)
    safe_message = _to_bmp_only(message) if CHROMEDRIVER_BMP_ONLY else message
    
    # 입력창
    chat = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea"))
    )
    chat.click()
    chat.clear()
    chat.send_keys(safe_message)

    # 보내기 버튼 (aria-label="보내기")
    send_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[aria-label="보내기"]')
        )
    )
    send_button.click()

    # 응답 완료 대기
    try:
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, AI_COMPLETE))
        )
    except TimeoutException:
        print("⚠ AI_COMPLETE 기다리다 타임아웃 (셀렉터 불일치/응답 지연 가능성)")
        raise

    print("✅ send_message 완료")


def copy_message_and_resend(driver, timeout: int = 30):
    """
    화면에 보이는 '복사' 버튼들 중 ★가장 마지막 것★만 클릭하여
    그 메시지를 입력창에 붙여넣고 다시 전송.
    (= simple, long, special 중 마지막으로 보낸 special만 복사)
    """
    wait = WebDriverWait(driver, timeout)

    # 1) 모든 '복사' 버튼 수집 후, 마지막 것만 선택
    copy_buttons = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'button[aria-label="복사"]')
        )
    )
    copy_btn = copy_buttons[-1]  # 🔥 가장 마지막 메시지의 복사 버튼
    copy_btn.click()
    print("✅ 마지막 메시지 복사 버튼 클릭 완료")

    # 2) 입력창에 포커스 주고 붙여넣기 (Ctrl+V)
    chat = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea"))
    )
    chat.click()
    chat.send_keys(Keys.CONTROL, "v")

    # 3) 보내기 버튼 클릭
    send_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[aria-label="보내기"]')
        )
    )
    send_button.click()

    # 4) AI 응답 완료 대기
    try:
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, AI_COMPLETE))
        )
    except TimeoutException:
        print("⚠ 복사→붙여넣기→전송 후 AI_COMPLETE 대기 타임아웃")
        raise

    print("✅ 복사한 마지막 메시지 재전송 완료")