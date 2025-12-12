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
"장문 문장 요약 입니다....《어린 왕자》는 프랑스 작가 생텍쥐페리가 1943년에 발표한 소설로, 겉보기에는 어린이 동화 같지만 인간의 본성과 삶, 사랑, 우정에 대한 깊은 성찰을 담고 있습니다. 이야기의 화자는 비행기 조종사로, 어린 시절 꿈꾸던 대로 사막에서 비행기를 수리하던 중 신비로운 소년, ‘어린 왕자’를 만나게 됩니다."
"어린 왕자는 자신이 살던 B-612 소행성을 떠나 여러 별들을 여행하며 다양한 어른들을 만납니다. 첫 번째 별에서는 왕을, 두 번째 별에서는 허영심 많은 사람, 세 번째 별에서는 술주정뱅이, 네 번째 별에서는 사업가, 다섯 번째 별에서는 가로등 켜는 사람, 여섯 번째 별에서는 지리학자를 만납니다. 각 인물은 어른들의 어리석음과 세속적 집착을 상징하며, 어린 왕자는 이를 이해하려 애쓰지만 때때로 답답해합니다."
"지구에 도착한 어린 왕자는 사막에서 조종사를 만나게 되고, 이야기는 그의 경험을 통해 인간관계와 삶의 의미를 탐구합니다. 지구에서 그는 장미꽃 한 송이를 기억하며, 그 꽃은 그가 사랑했던 존재이자, 책임과 소중함을 가르쳐 준 존재입니다. 장미꽃은 자만심과 허영심이 강하지만, 어린 왕자는 그녀를 위해 마음을 쓰고, 떠난 후에는 그 사랑의 의미를 깨닫습니다."
"어린 왕자는 또한 여우를 만나 길들임과 사랑의 본질을 배우게 됩니다. 여우는 “진정으로 중요한 것은 눈에 보이지 않는다”라고 말하며, 관계 속에서 책임과 유대가 얼마나 소중한지 가르쳐 줍니다. 이는 작품의 핵심 메시지 중 하나로, 외형적 가치보다 마음과 감정의 진실함을 강조합니다."
"어린 왕자는 결국 자신의 소행성과 장미꽃으로 돌아가기로 결심하며, 조종사에게 이별을 고합니다. 조종사는 어린 왕자와의 만남을 통해 순수함, 상상력, 사랑의 의미를 다시 깨닫게 되고, 인간 세계의 소중한 가치들을 성찰하게 됩니다. 어린 왕자는 신비롭게 사라지지만, 독자는 그의 이야기를 통해 삶과 인간관계에 대해 깊이 생각하게 됩니다."
"위 내용 한단어로 요약해줘"
)
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
# driver.quit()  # 필요 시 주석 해제
