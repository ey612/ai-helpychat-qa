from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains 
import time

# -------------------------------------------------------
#   ⭐ 실행
# -------------------------------------------------------
driver = webdriver.Chrome()
driver.get("https://qaproject.elice.io/ai-helpy-chat")

wait = WebDriverWait(driver, 10)
print("1. 홈페이지 접속 완료")

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
print("2. 로그인 완료")

time.sleep(3)  # 로딩 대기

# -------------------------------------------------------
#   ⭐ 메시지 전송 + AI 답변 완료 
# -------------------------------------------------------
def send_message(message):
    chat_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='input']"))
    )

    chat_input.send_keys(message)
    chat_input.send_keys(Keys.ENTER)
    print(f"메시지 전송 완료: {message[:10]}...")

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
#   ⭐ 페이지 이동 버튼 클릭
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
        
def click_next_answer():
    try:
        next_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 'button:has(svg[data-testid="chevron-rightIcon"])')
            )
        )
        next_btn.click()
        print("➡️ 다음 답변 페이지 이동")

        # 다음 페이지의 AI 답변 완료 대기
        ai_selector = 'div.elice-aichat__markdown[data-status="complete"]'
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ai_selector))
        )
        print("🤖 다음 답변 페이지 로딩 완료!\n")

    except Exception as e:
        print("⚠ 다음 페이지 이동 실패:", e)

# -------------------------------------------------------
#   ⭐ 질문 수정 버튼 클릭
# -------------------------------------------------------
        
def click_edit_button():
    try:
        # 마지막 메시지 span 가져오기
        last_msg_span = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'span[data-status="complete"]')
            )
        )[-1]

        # 메시지 span으로 hover
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", last_msg_span)
        ActionChains(driver).move_to_element(last_msg_span).perform()
        print("🖱 메시지 span에 마우스 hover 완료")

        time.sleep(1)  # hover 후 버튼 렌더링 대기

        # 수정 버튼 클릭
        edit_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="수정"]'))
        )
        driver.execute_script("arguments[0].click();", edit_btn)
        print("✏️ 수정 버튼 클릭 완료")
        
    except Exception as e:
        print("⚠ 수정 버튼 클릭 실패:", e)

def edit_textarea_message(new_text):
    try:
        # 1) textarea 요소가 나타날 때까지 대기
        edit_textarea = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[name='input']"))
        )

        # 2) scrollIntoView + 클릭해서 포커스 확보
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_textarea)
        edit_textarea.click()

        # 3) 기존 텍스트 삭제
        edit_textarea.clear()
        time.sleep(0.2)  # 잠시 대기

        # 4) 새 텍스트 입력
        edit_textarea.send_keys(new_text)
        print(f"📝 메시지 수정 완료: {new_text}")

        # 5) 엔터로 전송
        edit_textarea.send_keys(Keys.ENTER)
        print("📨 수정 메시지 전송 완료")

        # 6) AI 답변 완료 대기
        ai_selector = 'div.elice-aichat__markdown[data-status="complete"]'
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ai_selector))
        )
        print("🤖 AI 답변 완료!")

    except Exception as e:
        print("⚠ 메시지 수정 실패:", e)

# -------------------------------------------------------
#   ⭐ 테스트 실행
# -------------------------------------------------------
send_message("안녕하세요! 자동화 테스트 메시지입니다.")

send_message("")

long_msg = (
"장문 문장 요약 입니다..."*50)
send_message(long_msg)

# 다시 생성 실행
click_regenerate()

# 이전 답변 페이지 이동
click_prev_answer()

# 다음 답변 페이지 이동
click_next_answer()

#질문 수정 버튼 클릭
click_edit_button()

#수정 메시지 보내기
new_text = "수정 메시지 입니다."
edit_textarea_message(new_text)

print("🎉 모든 테스트 자동화 완료! 브라우저는 자동 종료되지 않습니다.")
# driver.quit()  # 필요 시 주석 해제



