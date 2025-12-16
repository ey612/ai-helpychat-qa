from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import AI_COMPLETE
import time

def click_edit_button(driver):
    last_msg = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'span[data-status="complete"]')
        )
    )[-1]

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});", last_msg
    )
    ActionChains(driver).move_to_element(last_msg).perform()
    time.sleep(1)

    edit_btn = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'button[aria-label="수정"]')
        )
    )
    driver.execute_script("arguments[0].click();", edit_btn)

    print("✏️ 질문 수정 버튼 클릭")

def edit_textarea_message(driver, new_text):
    textarea = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "textarea[name='input']")
        )
    )
    textarea.click()
    textarea.clear()
    textarea.send_keys(new_text)
    textarea.send_keys(Keys.ENTER)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, AI_COMPLETE))
    )

    print("📝 메시지 수정 완료")