# tests/test_signup_tc_001.py

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


def test_signup_tc_001(driver):
    """
    SIGNUP_TC_001
    회원가입 성공 케이스
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

    # 3) 회원정보 입력 (이메일은 매번 유니크)
    email_input = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@type='email' or @name='email' or @name='loginId']")
        )
    )
    unique_email = f"test{int(time.time())}@example.com"
    email_input.clear()
    email_input.send_keys(unique_email)

    password_input = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@type='password' or @name='password']")
        )
    )
    password_input.clear()
    password_input.send_keys("abcd!1234")

    name_input = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//input[@name='name' or @name='fullName' or contains(@placeholder, 'Name')]",
            )
        )
    )
    name_input.clear()
    name_input.send_keys("testname")

    # 4) 약관 전체 동의
    checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
    if checkboxes and not checkboxes[0].is_selected():
        checkboxes[0].click()

    # 5) 회원가입 버튼 클릭
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

    # 6) 성공 / 실패 판정
    # 실패: 중복 이메일 메시지
    duplicate_error_locator = (
        By.XPATH,
        "//*[contains(., 'already') and contains(., 'registered')]"
        " | //*[contains(., '이미') and (contains(., '등록') or contains(., '가입'))]"
    )

    # ✅ 성공: 'Nice to meet you again' 화면이 뜨면 성공
    # (로그인 히스토리 화면 제목 + Login 버튼 둘 중 하나라도 뜨면 성공으로 보게 안전하게 구성)
    nice_title_locator = (By.XPATH, "//*[contains(normalize-space(.), 'Nice to meet you again')]")
    login_button_locator = (By.XPATH, "//button[normalize-space(.)='Login']")

    def success_condition(d):
        return bool(d.find_elements(*nice_title_locator) or d.find_elements(*login_button_locator))

    try:
        WebDriverWait(driver, 10).until(
            lambda d: success_condition(d) or d.find_elements(*duplicate_error_locator)
        )
    except TimeoutException:
        assert False, "성공/실패 상태를 감지하지 못함 (페이지 전환 또는 메시지 없음)"

    # 실패 케이스
    if driver.find_elements(*duplicate_error_locator):
        assert False, f"회원가입 실패: 중복 이메일 메시지 표시됨 (email={unique_email})"

    # 성공 케이스
    assert success_condition(driver), (
        f"회원가입 성공 후 'Nice to meet you again' 화면이 감지되지 않음 (email={unique_email})"
    )

    print(
        f"\n🎉 테스트 성공! 회원가입이 정상 처리되었습니다. "
        f"(email={unique_email})\n"
    )
