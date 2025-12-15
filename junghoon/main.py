from login import setup_driver, login
from chat_actions import *

driver, wait = setup_driver()
login(driver, wait)

send_message(driver, "안녕하세요! 자동화 테스트 메시지입니다.")
send_message(driver, "")
send_message(driver, "장문 문장 요약 입니다..." * 50)

click_regenerate(driver)
click_prev_answer(driver)
click_next_answer(driver)

click_edit_button(driver)
edit_textarea_message(driver, "수정 메시지 입니다.")

print("🎉 모든 테스트 자동화 완료")