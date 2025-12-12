# tests/test_signup.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time

BASE_URL = "https://qaproject.elice.io/ai-helpy-chat"


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    yield driver
    time.sleep(3)
    driver.quit()


def test_signup_tc_001(driver):
    """
    SIGNUP_TC_001
    """
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 15)

    # 1) Create account 링크
    create_account_link = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href^='/accounts/signup']"))
    )
    create_account_link.click()

    # 2) Create account with email
    create_with_email_btn = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(., 'Create account with email')]"
                " | //button[contains(., 'Email') and contains(., 'account')]"
            )
        )
    )
    create_with_email_btn.click()

    # 3) 입력
    email_input = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@name='email' or @name='loginId' or @type='email']")
        )
    )
    email_input.send_keys("test001@example.com")

    password_input = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@name='password' or @type='password']")
        )
    )
    password_input.send_keys("Abc!1234")

    name_input = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//input[@name='name' or @name='fullName' or contains(@placeholder, 'Name')]",
            )
        )
    )
    name_input.send_keys("Hong Gil-dong")

    # 4) 약관 체크
    checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
    if checkboxes and not checkboxes[0].is_selected():
        checkboxes[0].click()

    # 5) 회원가입 제출
    submit_btn = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[@type='submit']"
                " | //button[contains(., 'Sign up')]"
                " | //button[contains(., 'Create account')]",
            )
        )
    )
    submit_btn.click()

    # 6) 가입 성공 여부 확인
    try:
        wait.until(EC.presence_of_element_located((By.NAME, "loginId")))
    except:
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='input']"))
        )

    # 🔥 테스트 성공 문구 출력
    print("\n🎉 테스트에 성공했습니다! 회원가입 절차가 정상 동작합니다.\n")
