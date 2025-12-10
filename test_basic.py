from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.get("https://accounts.elice.io/accounts/signin/history?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat&lang=en-US&org=qaproject")

wait = WebDriverWait(driver, 10)

# ⭐ 이메일 입력
email_input = wait.until(
    EC.presence_of_element_located((By.NAME, "loginId"))
)
email_input.send_keys("qa3team06@elicer.com")

# ⭐ 비밀번호 입력
password_input = wait.until(
    EC.presence_of_element_located((By.NAME, "password"))
)
password_input.send_keys("20qareset25elice!")

# ⭐ 로그인 버튼 클릭
login_button = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
)
login_button.click()

print("로그인 완료")

# ⭐ 페이지 로딩 대기
time.sleep(3)

# ⭐ 채팅 입력창 찾기 (확정된 선택자)
chat_input = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='input']"))
)

# 메시지 입력 및 전송
chat_message = "안녕하세요! 자동화 테스트 메시지입니다."
chat_input.send_keys(chat_message)
chat_input.send_keys(Keys.ENTER)

print("메시지 전송 완료")

time.sleep(2)

# ❌ 자동 종료 방지 — 주석 처리
# driver.quit()
