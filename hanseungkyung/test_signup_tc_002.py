# tests/test_signup_tc_002.py

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


def test_signup_tc_002(driver):
    """
    SIGNUP_TC_002
    이메일 미입력 시 회원가입 불가 + 안내 메시지 표시
    """
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 15)

    # 1) Create account 링크 클릭
    create_account_link = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href^='/accounts/signup']"))
    )
    create_account_link.click()

    # 2) Create account with email 클릭
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

    # 3) 입력 폼 로딩 대기
    email_input = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@type='email' or @name='email' or @name='loginId']")
        )
    )

    password_input = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@type='password' or @name='password']")
        )
    )

    name_input = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@name='name' or @name='fullName' or contains(@placeholder, 'Name')]")
        )
    )

    # 4) 이메일은 미입력(빈값 유지), 비밀번호/이름만 입력
    email_input.clear()

    password_input.clear()
    password_input.send_keys("abcd!1234")

    name_input.clear()
    name_input.send_keys("testname")

    # 5) 약관 전체 동의(첫 체크박스)
    checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
    if checkboxes and not checkboxes[0].is_selected():
        checkboxes[0].click()

    # 6) 회원가입 버튼 클릭
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

    # ---- 판정 로직 ----
    # A) 브라우저 기본 validation(Chrome) 메시지 확인 (required / type=email)
    #    - required가 걸려있으면 validationMessage가 비어있지 않음
    validation_msg = driver.execute_script(
        "return arguments[0].validationMessage;", email_input
    )

    # B) 페이지 내 에러 문구(필수/required/email 관련) 노출 확인(앱에서 자체 에러 렌더링하는 경우)
    email_required_error_locator = (
        By.XPATH,
        "//*[contains(translate(., 'EMAILREQUIRDFILSU', 'emailrequirdfilsu'), 'email') "
        "and (contains(translate(., 'REQUIRED', 'required'), 'required') "
        "or contains(., '필수') or contains(., '입력'))]"
        " | //*[contains(., '이메일') and (contains(., '필수') or contains(., '입력'))]"
    )

    def email_error_visible(d):
        return bool(d.find_elements(*email_required_error_locator))

    try:
        WebDriverWait(driver, 5).until(lambda d: (validation_msg and len(validation_msg) > 0) or email_error_visible(d))
    except TimeoutException:
        # 둘 다 못 잡으면, 최소한 가입 성공 화면으로 넘어가면 안 됨
        nice_title_locator = (By.XPATH, "//*[contains(normalize-space(.), 'Nice to meet you again')]")
        if driver.find_elements(*nice_title_locator):
            assert False, "이메일 미입력인데 가입 성공 화면으로 이동함(버그 가능)"
        assert False, "이메일 필수 입력 안내 메시지를 감지하지 못함"

    # 최종 Assert: (validationMessage 있거나) (페이지 에러 문구가 보이거나)
    assert (validation_msg and len(validation_msg) > 0) or email_error_visible(driver), (
        f"이메일 미입력 시 안내 메시지가 표시되지 않음 (validationMessage={validation_msg!r})"
    )

    print("\n✅ 테스트 성공! 이메일 미입력 시 가입이 차단되고 안내가 표시됨.\n")
