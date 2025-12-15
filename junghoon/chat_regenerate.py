from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import AI_COMPLETE, REGENERATE_BTN

def click_regenerate(driver):
    try:
        btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, REGENERATE_BTN))
        )
        btn.click()

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, AI_COMPLETE))
        )
        print("🔄 다시 생성 완료")

    except Exception as e:
        print("⚠ 다시 생성 실패:", e)