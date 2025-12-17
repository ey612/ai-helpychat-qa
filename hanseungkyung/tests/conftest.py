# tests/conftest.py
import sys
from pathlib import Path

# ✅ 1) 가장 먼저 프로젝트 루트를 sys.path에 추가
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ✅ 2) 그 다음에야 프로젝트 모듈 import 가능
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from driver_setup import driver  # noqa: F401
from constants import BASE_URL, LOGIN_EMAIL, LOGIN_PASSWORD


@pytest.fixture
def login(driver):
    driver.get(BASE_URL)

    wait = WebDriverWait(driver, 10)

    email_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )
    password_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
    )

    email_input.clear()
    email_input.send_keys(LOGIN_EMAIL)

    password_input.clear()
    password_input.send_keys(LOGIN_PASSWORD)

    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()

    # 로그인 성공 기준: 메시지 입력창(placeholder에 '메시지')
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(@placeholder,'메시지')]")))

    yield
