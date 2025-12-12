# tests/test_signup_tc_005.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pytest

BASE_URL = "https://qaproject.elice.io/ai-helpy-chat"


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    yield driver
    driver.quit()


def test_signup_tc_005(driver):
    """
    SIGNUP_TC_005
    잘못된 이메일 형식 입력 시 회원가입 불가 + 형식 오류 안내 표시
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

    # 잘못된 이메일 형식
    email_input.clear()
    email_input.send_keys("test@")  # invalid

    password_input.clear()
    password_input.send_keys("abcd!1234")

    name_input.clear()
    name_input.send_keys("testname")

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
    # A) 브라우저 기본 validation message (type=email)
    validation_msg = driver.execute_script("return arguments[0].validationMessage;", email_input)

    # B) 화면 내 이메일 형식 오류 문구
    invalid_email_error_locator = (
        By.XPATH,
        "//*[contains(., '이메일') and (contains(., '형식') or contains(., '올바르') or contains(., '유효'))]"
        " | //*[contains(translate(., 'INVALIDEMAILFORMAT', 'invalidemailformat'), 'email') "
        "and (contains(translate(., 'INVALID', 'invalid'), 'invalid') or contains(translate(., 'FORMAT', 'format'), 'format'))]"
    )

    def invalid_email_error_visible(d):
        return bool(d.find_elements(*invalid_email_error_locator))

    try:
        WebDriverWait(driver, 5).until(
            lambda d: (validation_msg and len(validation_msg) > 0) or invalid_email_error_visible(d)
        )
    except TimeoutException:
        nice_title_locator = (By.XPATH, "//*[contains(normalize-space(.), 'Nice to meet you again')]")
        if driver.find_elements(*nice_title_locator):
            assert False, "잘못된 이메일 형식인데 가입 성공 화면으로 이동함(버그 가능)"
        assert False, "이메일 형식 오류 안내를 감지하지 못함"

    assert (validation_msg and len(validation_msg) > 0) or invalid_email_error_visible(driver), (
        f"이메일 형식 오류 안내가 표시되지 않음 (validationMessage={validation_msg!r})"
    )

    print("\n✅ 테스트 성공! 잘못된 이메일 형식 입력 시 가입이 차단되고 안내가 표시됨.\n")
