from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import AI_COMPLETE

def send_message(driver, message):
    chat = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='input']"))
    )
    chat.send_keys(message)
    chat.send_keys(Keys.ENTER)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, AI_COMPLETE))
    )

    print(f"📨 메시지 전송 완료: {message[:10]}...")
