# signup/signup_actions.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from signup.signup_page import SignupPage


def open_signup_method_page(driver, wait):
    """
    로그인 첫 화면에서 'Create account' / 'Sign up' 진입 버튼을 눌러
    가입 방식 선택 화면으로 이동(버튼/링크 문구는 유연하게 처리)
    """
    candidates = [
        (By.XPATH, "//button[contains(., 'Create account') or contains(., 'Sign up')]"),
        (By.XPATH, "//a[contains(., 'Create account') or contains(., 'Sign up')]"),
    ]

    clicked = False
    for by, xp in candidates:
        elems = driver.find_elements(by, xp)
        if elems:
            elems[0].click()
            clicked = True
            break

    if not clicked:
        # 화면 구조가 다를 수 있으니, 최소한 method 버튼이 나타날 때까지 대기
        pass

    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//button[contains(., 'Create account with email')]")
    ))


def open_signup_email_form(driver, wait):
    open_signup_method_page(driver, wait)
    btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(., 'Create account with email')]")
    ))
    btn.click()


def get_signup_inputs(wait):
    email = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email' or @name='email' or @name='loginId']")))
    pw = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password' or @name='password']")))
    name = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder,'Name') or @name='name' or @name='fullName']")))
    return email, pw, name


def check_terms_1to3_only(driver, wait):
    # 약관 펼치기(있으면)
    headers = driver.find_elements(By.ID, "agreement-header")
    if headers:
        header = headers[0]
        if header.get_attribute("aria-expanded") != "true":
            driver.execute_script("arguments[0].click();", header)

    # 체크박스들(있으면)
    cbs = driver.find_elements(By.XPATH, "//div[@id='agreement-contents']//input[@type='checkbox']")
    if not cbs:
        # 페이지에 약관이 없거나 구조가 다르면 그냥 반환
        return

    # 1~3 체크, 나머지 해제
    for i, cb in enumerate(cbs):
        should_check = i in (0, 1, 2)
        if should_check and not cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)
        if (not should_check) and cb.is_selected():
            driver.execute_script("arguments[0].click();", cb)


def click_submit(wait):
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    btn.click()


def unique_email():
    return f"test{int(time.time())}@example.com"
