from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# -------------------------------------------------------
#   ⭐ 드라이버 실행
# -------------------------------------------------------
driver = webdriver.Chrome()
driver.get("https://qaproject.elice.io/ai-helpy-chat")

wait = WebDriverWait(driver, 10)
print("홈페이지 접속 완료")

# -------------------------------------------------------
#   ⭐ 로그인
# -------------------------------------------------------
email_input = wait.until(
    EC.presence_of_element_located((By.NAME, "loginId"))
)
email_input.send_keys("qa3team06@elicer.com")

password_input = wait.until(
    EC.presence_of_element_located((By.NAME, "password"))
)
password_input.send_keys("20qareset25elice!")

login_button = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
)
login_button.click()
print("로그인 완료")

time.sleep(3)  # 로딩 대기

# -------------------------------------------------------
#   ⭐ 메시지 전송 + AI 답변 완료 감지 함수
# -------------------------------------------------------
def send_message(message):
    chat_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='input']"))
    )

    chat_input.send_keys(message)
    chat_input.send_keys(Keys.ENTER)
    print(f"메시지 전송 완료: {message[:20]}...")

    # AI 답변 완료 감지
    ai_selector = 'div.elice-aichat__markdown[data-status="complete"]'
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ai_selector))
    )

    print("🤖 AI 답변 완료!\n")
    time.sleep(1)

# -------------------------------------------------------
#   ⭐ 다시 생성 버튼 클릭
# -------------------------------------------------------
def click_regenerate():
    try:
        regen_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[aria-label='다시 생성']")
            )
        )
        regen_btn.click()
        print("🔄 다시 생성 버튼 클릭 완료")

        ai_selector = 'div.elice-aichat__markdown[data-status="complete"]'
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ai_selector))
        )
        print("🤖 다시 생성된 답변 완료!\n")

    except Exception as e:
        print("⚠ 다시 생성 버튼 클릭 실패:", e)

# -------------------------------------------------------
#   ⭐ 이전 답변 페이지 이동 버튼 클릭
# -------------------------------------------------------
def click_prev_answer():
    try:
        prev_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 'button:has(svg[data-testid="chevron-leftIcon"])')
            )
        )
        prev_btn.click()
        print("⬅️ 이전 답변 페이지 이동")

        ai_selector = 'div.elice-aichat__markdown[data-status="complete"]'
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ai_selector))
        )
        print("🤖 이전 답변 페이지 로딩 완료!\n")

    except Exception as e:
        print("⚠ 이전 페이지 이동 실패:", e)

# -------------------------------------------------------
#   ⭐ 테스트 실행
# -------------------------------------------------------
send_message("안녕하세요! 자동화 테스트 메시지입니다.")

long_msg = (
    "《어린 왕자》 내용 요약해줘. "
    "위 내용 한 단어로 말해줘."
)
send_message(long_msg)

# 다시 생성 실행
click_regenerate()

# 이전 답변 페이지 이동
click_prev_answer()

print("🎉 모든 테스트 자동화 완료! 브라우저는 자동 종료되지 않습니다.")
# driver.quit()  # 필요 시 주석 해제
