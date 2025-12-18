from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def init_driver():
    driver = webdriver.Chrome()
    driver.get("https://qaproject.elice.io/ai-helpy-chat")
    wait = WebDriverWait(driver, 10)
    print("1. 홈페이지 접속 완료")
    return driver, wait

def login(driver, wait):
    wait.until(EC.presence_of_element_located((By.NAME, "loginId"))).send_keys(
        "qa3team06@elicer.com"
    )
    wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(
        "team06cheerup!"
    )
    wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    ).click()

    time.sleep(3)
    print("2. 로그인 완료")