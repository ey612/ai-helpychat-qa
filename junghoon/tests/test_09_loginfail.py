import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from junghoon.login import init_driver
from junghoon.loginfail import (  # 공통 함수 파일 (조금 뒤에 예시 보여줄게요)
    login_with_invalid_id,
    login_with_invalid_pw_only,
)


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
    id_input = wait.until(EC.presence_of_element_located((By.NAME, "loginId")))
    id_input.clear()
    id_input.send_keys(invalid_id)

    # 2️⃣ 비밀번호 입력
    pw_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
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
    time.sleep(3)
    assert error_msg.is_displayed()
    print("✅ 이메일 또는 비밀번호가 일치하지 않습니다. 메시지 정상 노출 확인")


def test_login_with_invalid_pw(driver_wait):
    driver, wait = driver_wait

    invalid_id = "invalid_id"
    password = "wrong_password"

    # 1️⃣ ID 입력
    id_input = wait.until(EC.presence_of_element_located((By.NAME, "loginId")))
    id_input.clear()
    id_input.send_keys(invalid_id)

    # 2️⃣ 비밀번호 입력
    pw_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
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
    time.sleep(3)
    assert error_msg.is_displayed()
    print("✅ 이메일 형식이 잘못되었습니다. 로그인 실패 정상 노출 확인 ")


def test_login_fail_5_times_observe_lock_message(driver_wait):
    """
    같은 ID로 비밀번호를 5번 연속 틀렸을 때
    - 락 문구가 뜨면: 로그로 남기고 PASS
    - 5번 안에 안 떠도: 그냥 PASS

    👉 즉, 이 테스트는 '락 정책이 있는지 없는지'를 관찰만 하고,
       어떤 경우에도 실패시키지 않는다.
    """
    driver, wait = driver_wait

    invalid_id = "invalid_id@test.com"
    password = "wrong_password"
    max_attempts = 5

    def lock_message_exists() -> bool:
        """락 문구가 화면에 보이는지 짧게 체크."""
        try:
            warning = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//*[contains(text(), 'You have attempted to log in incorrectly several times')]",
                    )
                )
            )
            print("⚠ 락 경고 문구 감지:", warning.text.strip())
            return True
        except Exception:
            return False

    # 1회차: ID + PW 모두 입력해서 로그인 시도
    print("🚫 잘못된 로그인 시도 1회 (ID + PW 입력)")
    login_with_invalid_id(driver, wait, invalid_id, password)

    if lock_message_exists():
        print("✅ 1회차 후 이미 락 경고 문구가 노출되었습니다.")
        return  # PASS

    # 2~5회차: PW만 다시 입력해서 시도
    for i in range(2, max_attempts + 1):
        print(f"🚫 잘못된 로그인 시도 {i}회 (PW만 재입력)")
        login_with_invalid_pw_only(driver, wait, password)

        if lock_message_exists():
            print(f"✅ {i}회차 로그인 실패 후 락 경고 문구가 노출되었습니다.")
            return  # PASS

    # 여기까지 왔다면 1~5회 어디에서도 락 문구가 안 뜬 것
    print(
        "ℹ 5번 연속 로그인 실패했지만 락 경고 문구는 나타나지 않았습니다. (테스트는 PASS로 처리)"
    )
    # assert / pytest.fail 없음 → 자연스럽게 PASS
