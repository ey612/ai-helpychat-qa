from login import init_driver, login
from chat_sendmessage import send_message
from chat_regenerate import click_regenerate
from chat_navigarion import click_prev_answer, click_next_answer
from chat_editmessage import click_edit_button, edit_textarea_message
from selenium import webdriver
from chat_history import ChatHistoryManager
from chat_history_delete import delete_history
from logout import logout
import time
driver, wait = init_driver()

try:
    login(driver, wait)

    send_message(driver, "안녕하세요 자동화 테스트입니다.")
    time.sleep(2)
    send_message(driver, "장문 요약 입니다!!."*90)
    time.sleep(2)
    click_regenerate(driver, index=1)
    time.sleep(2)
    click_prev_answer(driver)
    time.sleep(2)
    click_next_answer(driver)
    time.sleep(2)
    click_edit_button(driver)
    time.sleep(2)
    edit_textarea_message(driver, "수정 메시지 입니다.")
    time.sleep(2)
# 채팅 히스토리 클릭
    history = ChatHistoryManager(driver)
    time.sleep(2)
    history.rename_history_and_save(
    "안녕하세요 자동화 테스트입니다.",           # 기존 제목(히스토리에서 보이는 텍스트 일부)
    "이름 변경 완료"  # 새 제목
    )
    time.sleep(2)
    delete_history(driver, "이름 변경 완료")
    time.sleep(2)
    logout(driver)
    time.sleep(2)
    print("🎉 전체 자동화 시나리오 완료")

except Exception as e:
    print("⚠ 테스트 중 오류 발생:", e)
    
print("🎉브라우저를 계속 유지합니다.")
input("브라우저를 닫으려면 Enter를 누르세요...")

    # driver.quit() 
