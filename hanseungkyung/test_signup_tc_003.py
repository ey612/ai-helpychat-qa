# tests/test_signup_tc_003.py

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


def test_signup_tc_003(driver):
    """
    SIGNUP_TC_003
    비밀번호 미입력 시 회원가입 불가 + 안내 메시지 표시
    """
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 15)

    # 1) Create account 링크 클릭
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href^='/accounts/signup']"))).click()

    # 2) Create accoun
