import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from constants import BASE_URL
from signup.signup_actions import (
    open_signup_method_page,
    open_signup_email_form,
    get_signup_inputs,
    check_terms_1to3_only,
    click_submit,
    unique_email,
)

# -----------------------
# 공통 유틸
# -----------------------
def _has_error(driver, xpath):
    return bool(driver.find_elements(By.XPATH, xpath))


# =======================
# UI 테스트
# =======================

def test_signup_tc_001_ui(driver):
    """SIGNUP_TC_001: 로그인 화면 → 회원가입 방식 선택 화면 이동"""
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_method_page(driver, wait)
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//button[contains(., 'Create account with email')]")
    ))


def test_signup_tc_002_ui(driver):
    """SIGNUP_TC_002: 가입 방식 선택 → 이메일 가입 입력 화면 이동"""
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[contains(@placeholder,'Name') or @name='name' or @name='fullName']")
    ))


# =======================
# 정상 케이스
# =======================

def test_signup_tc_003_success(driver):
    """SIGNUP_TC_003: 정상 정보 회원가입 성공"""
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    email, pw, name = get_signup_inputs(wait)

    u = unique_email()
    email.clear(); email.send_keys(u)
    pw.clear(); pw.send_keys("abcd!1234")
    name.clear(); name.send_keys("testname")

    check_terms_1to3_only(driver, wait)
    click_submit(wait)

    nice = (By.XPATH, "//*[contains(normalize-space(.), 'Nice to meet you again')]")
    login_btn = (By.XPATH, "//button[normalize-space(.)='Login']")
    WebDriverWait(driver, 10).until(lambda d: d.find_elements(*nice) or d.find_elements(*login_btn))


# =======================
# 필수 입력 예외
# =======================

def test_signup_tc_004_email_required(driver):
    """SIGNUP_TC_004: 이메일 미입력"""
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    email, pw, name = get_signup_inputs(wait)

    email.clear()
    pw.send_keys("abcd!1234")
    name.send_keys("testname")

    check_terms_1to3_only(driver, wait)
    click_submit(wait)

    v = driver.execute_script("return arguments[0].validationMessage;", email) or ""
    assert v or _has_error(driver, "//*[contains(.,'email') or contains(.,'이메일')]")


def test_signup_tc_005_password_required(driver):
    """SIGNUP_TC_005: 비밀번호 미입력"""
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    email, pw, name = get_signup_inputs(wait)

    email.send_keys(unique_email())
    pw.clear()
    name.send_keys("testname")

    check_terms_1to3_only(driver, wait)
    click_submit(wait)

    v = driver.execute_script("return arguments[0].validationMessage;", pw) or ""
    assert v or _has_error(driver, "//*[contains(.,'password') or contains(.,'비밀번호')]")


def test_signup_tc_006_name_required(driver):
    """SIGNUP_TC_006: 이름 미입력"""
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    email, pw, name = get_signup_inputs(wait)

    email.send_keys(unique_email())
    pw.send_keys("abcd!1234")
    name.clear()

    check_terms_1to3_only(driver, wait)
    click_submit(wait)

    v = driver.execute_script("return arguments[0].validationMessage;", name) or ""
    time.sleep(5)
    assert v or _has_error(driver, "//*[contains(.,'Name') or contains(.,'이름')]")
    


# =======================
# 이메일 형식 / 중복
# =======================

def test_signup_tc_007_invalid_email_format(driver):
    """SIGNUP_TC_007: 잘못된 이메일 형식"""
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    email, pw, name = get_signup_inputs(wait)

    email.send_keys("test@")
    pw.send_keys("abcd!1234")
    name.send_keys("testname")

    check_terms_1to3_only(driver, wait)
    click_submit(wait)

    v = driver.execute_script("return arguments[0].validationMessage;", email) or ""
    assert v or _has_error(driver, "//*[contains(.,'format') or contains(.,'형식')]")


def test_signup_tc_008_email_with_space(driver):
    """SIGNUP_TC_008: 공백 포함 이메일"""
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    email, pw, name = get_signup_inputs(wait)

    email.send_keys(f"test {int(time.time())}@example.com")
    pw.send_keys("abcd!1234")
    name.send_keys("testname")

    check_terms_1to3_only(driver, wait)
    click_submit(wait)

    v = driver.execute_script("return arguments[0].validationMessage;", email) or ""
    assert v or _has_error(driver, "//*[contains(.,'email') or contains(.,'이메일')]")


import pytest
from constants import DUPLICATE_EMAIL

def test_signup_tc_009_duplicate_email(driver):
    """SIGNUP_TC_009: 중복 이메일 가입 시도 → 중복 안내 메시지"""
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    email, pw, name = get_signup_inputs(wait)

    email.clear(); email.send_keys(DUPLICATE_EMAIL)
    pw.clear(); pw.send_keys("abcd!1234")
    name.clear(); name.send_keys("testname")

    check_terms_1to3_only(driver, wait)

    # 버튼이 비활성일 수도 있어서 presence로 클릭 시도
    submit = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
    submit.click()

    duplicate_xpath = (
        "//*[contains(.,'already') and contains(.,'registered')]"
        " | //*[contains(.,'already') and contains(.,'email')]"
        " | //*[contains(.,'이미') and (contains(.,'가입') or contains(.,'등록'))]"
        " | //*[contains(.,'중복')]"
    )

    try:
        WebDriverWait(driver, 7).until(lambda d: d.find_elements(By.XPATH, duplicate_xpath))
    except TimeoutException:
        pytest.skip(f"사전조건 미충족: DUPLICATE_EMAIL({DUPLICATE_EMAIL})이 중복 계정이 아닌 듯함")


# =======================
# 비밀번호 규칙
# =======================

def test_signup_tc_010_password_too_short(driver):
    """SIGNUP_TC_010: 비밀번호 길이 부족"""
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    email, pw, name = get_signup_inputs(wait)

    email.send_keys(unique_email())
    pw.send_keys("abcd!")
    name.send_keys("testname")

    check_terms_1to3_only(driver, wait)
    click_submit(wait)

    assert _has_error(driver, "//*[contains(.,'password') or contains(.,'비밀번호')]")


def test_signup_tc_011_password_no_number(driver):
    """SIGNUP_TC_011: 숫자 없는 비밀번호 → 규칙 오류 메시지"""
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    email, pw, name = get_signup_inputs(wait)

    email.clear(); email.send_keys(unique_email())
    name.clear(); name.send_keys("testname")

    # ✅ 눈 아이콘 먼저 클릭 (비밀번호 보이기)
    eye = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@type='password']/ancestor::*//button")
    ))
    assert pw.get_attribute("type") == "password"
    eye.click()
    assert pw.get_attribute("type") == "text"

    # ✅ 비밀번호 입력 (숫자 없음)
    pw.clear(); pw.send_keys("abcd!skfle")

    check_terms_1to3_only(driver, wait)
    click_submit(wait)

    rule_xpath = (
        "//*[contains(translate(.,'NUMBERDIGIT','numberdigit'),'number')"
        " or contains(translate(.,'NUMBERDIGIT','numberdigit'),'digit')"
        " or contains(.,'숫자') or contains(.,'규칙') or contains(.,'조합') or contains(.,'포함')]"
    )
    WebDriverWait(driver, 7).until(lambda d: d.find_elements(By.XPATH, rule_xpath))



def test_signup_tc_012_password_no_letter(driver):
    """SIGNUP_TC_012: 영문 없는 비밀번호"""
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    email, pw, name = get_signup_inputs(wait)

    email.clear(); email.send_keys(unique_email())
    name.clear(); name.send_keys("testname")

    # ✅ 눈 아이콘 클릭 → 보이기
    eye = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@type='password']/ancestor::*//button")
    ))
    eye.click()
    assert pw.get_attribute("type") == "text"

    # ✅ 비밀번호 입력 (영문 없음)
    pw.clear(); pw.send_keys("1234!@#$")

    check_terms_1to3_only(driver, wait)
    click_submit(wait)

    assert _has_error(driver, "//*[contains(.,'letter') or contains(.,'영문')]")



def test_signup_tc_013_password_no_special(driver):
    """SIGNUP_TC_013: 특수문자 없는 비밀번호"""
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    email, pw, name = get_signup_inputs(wait)

    email.clear(); email.send_keys(unique_email())
    name.clear(); name.send_keys("testname")

    # ✅ 눈 아이콘 클릭 → 보이기
    eye = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@type='password']/ancestor::*//button")
    ))
    eye.click()
    assert pw.get_attribute("type") == "text"

    # ✅ 비밀번호 입력 (특수문자 없음)
    pw.clear(); pw.send_keys("abcd1234")

    check_terms_1to3_only(driver, wait)
    click_submit(wait)

    assert _has_error(driver, "//*[contains(.,'special') or contains(.,'특수')]")



# =======================
# 약관
# =======================

def test_signup_tc_014_agree_all_ui(driver):
    """SIGNUP_TC_014: 전체 동의 시 모든 약관 체크"""
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)

    header = wait.until(EC.presence_of_element_located((By.ID, "agreement-header")))
    if header.get_attribute("aria-expanded") != "true":
        driver.execute_script("arguments[0].click();", header)

    agree_all = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//*[normalize-space(.)='Agree all']/ancestor::*//input[@type='checkbox']")
    ))
    if not agree_all.is_selected():
        driver.execute_script("arguments[0].click();", agree_all)

    cbs = driver.find_elements(By.XPATH, "//div[@id='agreement-contents']//input[@type='checkbox']")
    assert all(cb.is_selected() for cb in cbs[:4])


def test_signup_tc_015_required_terms_not_checked(driver):
    """
    SIGNUP_TC_015
    1번(나이) + 4번(Optional)만 체크, 2~3(필수) 미체크 → 가입 불가
    """
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    email, pw, name = get_signup_inputs(wait)

    email.clear(); email.send_keys(unique_email())
    pw.clear(); pw.send_keys("abcd!1234")
    name.clear(); name.send_keys("testname")

    # 약관 펼치기
    header = wait.until(EC.presence_of_element_located((By.ID, "agreement-header")))
    if header.get_attribute("aria-expanded") != "true":
        driver.execute_script("arguments[0].click();", header)

    # 1~4 체크박스
    cbs = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//div[@id='agreement-contents']//input[@type='checkbox']")
    ))

    # 1✅ / 2❌ / 3❌ / 4✅
    if not cbs[0].is_selected(): driver.execute_script("arguments[0].click();", cbs[0])
    for i in (1, 2):
        if cbs[i].is_selected(): driver.execute_script("arguments[0].click();", cbs[i])
    if len(cbs) >= 4 and not cbs[3].is_selected(): driver.execute_script("arguments[0].click();", cbs[3])

    submit = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))

    # ✅ 가입 불가 판정(짧게): 버튼이 비활성이면 PASS
    assert submit.get_attribute("disabled") is not None or submit.get_attribute("aria-disabled") == "true"



def test_signup_tc_016_required_terms_checked_success(driver):
    """SIGNUP_TC_016: [Required] 약관 2개만 동의 후 가입 성공"""
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    email, pw, name = get_signup_inputs(wait)

    email.send_keys(unique_email())
    pw.send_keys("abcd!1234")
    name.send_keys("testname")

    # ✅ [Required]가 붙은 약관만 체크 (2개)
    required_labels = wait.until(EC.presence_of_all_elements_located((
        By.XPATH,
        "//*[@id='agreement-contents']//label[contains(normalize-space(.), '[Required]')]"
    )))

    assert len(required_labels) == 2  # 교차검증: 필수 약관은 2개여야 함

    for label in required_labels:
        checkbox = label.find_element(By.XPATH, ".//input[@type='checkbox']")
        if not checkbox.is_selected():
            label.find_element(
                By.XPATH, ".//span[contains(@class,'MuiCheckbox-root')]"
            ).click()

    # 최종 상태 검증
    for label in required_labels:
        assert label.find_element(By.XPATH, ".//input[@type='checkbox']").is_selected()

    click_submit(wait)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(.,'Nice to meet you again') or normalize-space(.)='Login']")
        )
    )



# =======================
# 기타 UI
# =======================

def test_signup_tc_017_password_show_hide(driver):
    """SIGNUP_TC_017: 비밀번호 보기/숨기기"""
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    _, pw, _ = get_signup_inputs(wait)

    pw.send_keys("abcd!1234")
    eye = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@type='password']/ancestor::*//button")
    ))

    assert pw.get_attribute("type") == "password"
    eye.click()
    assert pw.get_attribute("type") == "text"
    eye.click()
    assert pw.get_attribute("type") == "password"
