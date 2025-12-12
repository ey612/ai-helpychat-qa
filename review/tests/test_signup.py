from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.signup_page import SignupPage

BASE_URL = "https://qaproject.elice.io/ai-helpy-chat"


def test_signup_tc_001(driver):
    """
    SIGNUP_TC_001
    """
    driver.get(BASE_URL)
    signup_page = SignupPage(driver)

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
                " | //button[contains(., 'Email') and contains(., 'account')]",
            )
        )
    )
    create_with_email_btn.click()

    signup_page.signup(
        email="test001@example.com", password="Abc!1234", name="Hong Gil-dong"
    )

    # 6) 가입 성공 여부 확인
    try:
        wait.until(EC.presence_of_element_located((By.NAME, "loginId")))
    except:
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='input']"))
        )

    # 🔥 테스트 성공 문구 출력
    print("\n🎉 테스트에 성공했습니다! 회원가입 절차가 정상 동작합니다.\n")
