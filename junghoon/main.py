from login import init_driver, login
from chat_sendmessage import send_message
from chat_regenerate import click_regenerate
from chat_navigarion import click_prev_answer, click_next_answer
from chat_editmessage import click_edit_button, edit_textarea_message

driver, wait = init_driver()
login(driver, wait)

send_message(driver, "안녕하세요 자동화 테스트입니다.")
send_message(driver, "장문 요약 입니다!!."*50)
click_regenerate(driver)
click_prev_answer(driver)
click_next_answer(driver)

click_edit_button(driver)
edit_textarea_message(driver, "수정 메시지 입니다.")

print("🎉 전체 자동화 시나리오 완료")
input("엔터를 누르면 종료합니다...")
driver.quit()