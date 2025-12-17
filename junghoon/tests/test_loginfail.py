import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from junghoon.login import init_driver


@pytest.fixture
def driver_wait():
    driver, wait = init_driver()
    yield driver, wait
    driver.quit()


def test_login_with_invalid_id(driver_wait):
    driver, wait = driver_wait

    invalid_id = "invalid_id@test.com"
    password = "wrong_password"

    # 1️⃣ ID 입력
    id_input = wait.until(
        EC.presence_of_element_located((By.NAME, "loginId"))
    )
    id_input.clear()
    id_input.send_keys(invalid_id)

    # 2️⃣ 비밀번호 입력
    pw_input = wait.until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    pw_input.clear()
    pw_input.send_keys(password)

    # 3️⃣ 로그인 버튼 클릭
    login_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    login_button.click()

    # 4️⃣ 실패 메시지 검증 ✅
    error_msg = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[text()='Email or password does not match']")
        )
    )

    assert error_msg.is_displayed()
    print("✅ 이메일 또는 비밀번호가 일치하지 않습니다. 메시지 정상 노출 확인")
    
def test_login_with_invalid_pw(driver_wait):
    driver, wait = driver_wait

    invalid_id = "invalid_id"
    password = "wrong_password"

    # 1️⃣ ID 입력
    id_input = wait.until(
        EC.presence_of_element_located((By.NAME, "loginId"))
    )
    id_input.clear()
    id_input.send_keys(invalid_id)

    # 2️⃣ 비밀번호 입력
    pw_input = wait.until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    pw_input.clear()
    pw_input.send_keys(password)

    # 3️⃣ 로그인 버튼 클릭
    login_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    login_button.click()

    # 4️⃣ 실패 메시지 검증 ✅
    error_msg = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[text()='Invalid email format.']")
        )
    )

    assert error_msg.is_displayed()
    print("✅이메일 형식이 잘못되었습니다. 로그인 실패 정상 노출 확인 ")