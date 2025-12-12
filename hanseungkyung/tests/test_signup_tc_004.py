# tests/test_signup_tc_004.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pytest
import time

BASE_URL = "https://qaproject.elice.io/ai-helpy-chat"


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    yield driver
    driver.quit()


def test_signup_tc_004(driver):
    """
    SIGNUP_TC_004
    이름 미입력 시 회원가입 불가 + 안내 메시지 표시
    """
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 15)

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href^='/accounts/signup']"))).click()

    wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(., 'Create account with email')]"
                " | //button[contains(., 'Email') and contains(., 'account')]"
            )
        )
    ).click()

    email_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='email' or @name='email' or @name='loginId']"))
    )
    password_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='password' or @name='password']"))
    )
    name_input = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@name='name' or @name='fullName' or contains(@placeholder, 'Name')]")
        )
    )

    # 이메일/비번만 입력, 이름은 미입력
    unique_email = f"test{int(time.time())}@example.com"
    email_input.clear()
    email_input.send_keys(unique_email)

    password_input.clear()
    password_input.send_keys("abcd!1234")

    name_input.clear()  # 비워둠

    checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
    if checkboxes and not checkboxes[0].is_selected():
        checkboxes[0].click()

    submit_btn = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[@type='submit'] | //button[contains(., 'Sign up')] | //button[contains(., 'Create account')]",
            )
        )
    )
    submit_btn.click()

    # ---- 판정 로직 ----
    validation_msg = driver.execute_script("return arguments[0].validationMessage;", name_input)

    name_required_error_locator = (
        By.XPATH,
        "//*[contains(., '이름') and (contains(., '필수') or contains(., '입력'))]"
        " | //*[contains(translate(., 'NAMEFULLNAMEREQUIRED', 'namefullnamerequired'), 'name') "
        "and contains(translate(., 'REQUIRED', 'required'), 'required')]"
    )

    def name_error_visible(d):
        return bool(d.find_elements(*name_required_error_locator))

    try:
        WebDriverWait(driver, 5).until(lambda d: (validation_msg and len(validation_msg) > 0) or name_error_visible(d))
    except TimeoutException:
        nice_title_locator = (By.XPATH, "//*[contains(normalize-space(.), 'Nice to meet you again')]")
        if driver.find_elements(*nice_title_locator):
            assert False, "이름 미입력인데 가입 성공 화면으로 이동함(버그 가능)"
        assert False, "이름 필수 안내 메시지를 감지하지 못함"

    assert (validation_msg and len(validation_msg) > 0) or name_error_visible(driver), (
        f"이름 미입력 안내가 표시되지 않음 (validationMessage={validation_msg!r})"
    )

    print("\n✅ 테스트 성공! 이름 미입력 시 가입이 차단되고 안내가 표시됨.\n")
