from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .constants import AI_COMPLETE, PREV_BTN, NEXT_BTN

def click_prev_answer(driver):
    btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, PREV_BTN))
    )
    btn.click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, AI_COMPLETE))
    )
    print("⬅️ 이전 답변 이동")

def click_next_answer(driver):
    btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, NEXT_BTN))
    )
    btn.click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, AI_COMPLETE))
    )
    print("➡️ 다음 답변 이동")
