import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def open_signup_method_page(driver, wait):
    # 로그인 화면 → 가입 방식 선택 화면
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href^='/accounts/signup']"))).click()


def open_signup_email_form(driver, wait):
    # 가입 방식 선택 화면 → 이메일 가입 폼
    open_signup_method_page(driver, wait)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Create account with email')]"))).click()


def get_signup_inputs(wait):
    email = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
    pw = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
    name = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[contains(@placeholder,'Name') or @name='name' or @name='fullName']")
        )
    )
    return email, pw, name


def check_terms_1to3_only(driver, wait):
    # ▼ 펼치기
    header = wait.until(EC.presence_of_element_located((By.ID, "agreement-header")))
    if header.get_attribute("aria-expanded") != "true":
        driver.execute_script("arguments[0].click();", header)

    # 약관 1~4 체크박스(순서대로)
    cbs = wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//div[@id='agreement-contents']//input[@type='checkbox']")
        )
    )

    # 1~3만 체크
    for i in range(3):
        if not cbs[i].is_selected():
            driver.execute_script("arguments[0].click();", cbs[i])

    # 4(Optional) 해제(방어)
    if len(cbs) >= 4 and cbs[3].is_selected():
        driver.execute_script("arguments[0].click();", cbs[3])


def click_submit(wait):
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()


def unique_email():
    return f"test{int(time.time())}@example.com"
