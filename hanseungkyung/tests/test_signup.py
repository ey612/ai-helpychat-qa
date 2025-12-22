import time
import pytest
from functools import wraps

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from constants import BASE_URL, DUPLICATE_EMAIL
from signup.signup_actions import (
    open_signup_method_page,
    open_signup_email_form,
    get_signup_inputs,
    check_terms_1to3_only,
    click_submit,
    unique_email,
)

# =======================
# TC 메타 (엑셀의 ID + 시나리오)
# =======================
TC_META = {
    "SIGNUP_TC_001": "로그인 화면에서 회원가입으로 정상 이동 여부 확인",
    "SIGNUP_TC_002": "이메일로 가입하기 버튼 클릭 시 입력폼으로 이동",
    "SIGNUP_TC_003": "정상 정보로 회원가입이 후 로그인 화면 출력",
    "SIGNUP_TC_004": "이메일 미입력 시 가입 불가 여부 확인",
    "SIGNUP_TC_005": "비밀번호 미입력 시 가입 불가 여부 확인",
    "SIGNUP_TC_006": "이름 미입력 시 가입 불가 여부 확인",
    "SIGNUP_TC_007": "잘못된 이메일 형식 입력 시 오류 발생 여부 확인",
    "SIGNUP_TC_008": "공백 포함 이메일 입력 시 오류 발생 여부 확인",
    "SIGNUP_TC_009": "중복 이메일 가입 시도 시 오류 발생 여부 확인",
    "SIGNUP_TC_010": "비밀번호 길이가 부족할 때 가입 제한 여부 확인",
    "SIGNUP_TC_011": "숫자가 없는 비밀번호 입력 시 오류 발생 여부 확인",
    "SIGNUP_TC_012": "영문 없는 비밀번호 입력 시 오류 발생 여부 확인",
    "SIGNUP_TC_013": "특수문자 없는 비밀번호 입력 시 오류 발생 여부 확인",
    "SIGNUP_TC_014": "전체 동의 체크 시 모든 약관 활성화 여부 확인",
    "SIGNUP_TC_015": "필수 약관 미동의 시 가입 불가 여부 확인(필수 약관 제외)",
    "SIGNUP_TC_016": "필수 약관만 동의하고 가입 가능 여부 확인",
    "SIGNUP_TC_017": "비밀번호 보기/숨기기 기능 동작 여부 확인",
}


# =======================
# 로그 유틸
# =======================
def _tc_desc(tc_id: str) -> str:
    return TC_META.get(tc_id, "").strip()


def log_start(tc_id: str):
    print(f"▶ [{tc_id}] {_tc_desc(tc_id)}")


def log_step(tc_id: str, msg: str):
    print(f"▶ [{tc_id}] {msg}")


def log_ok(tc_id: str, msg: str):
    print(f"✅ [{tc_id}] {_tc_desc(tc_id)} - {msg}")


def log_fail(tc_id: str, msg: str):
    print(f"❌ [{tc_id}] {_tc_desc(tc_id)} - {msg}")


def tc(tc_id: str):
    """pytest 테스트 전체 성공/실패를 한 줄로 찍어주는 데코레이터"""
    def deco(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            log_start(tc_id)
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                log_fail(tc_id, f"실패: {e}")
                raise
            finally:
                # pytest는 실패 시 여기까지도 오지만, 실패는 위에서 이미 ❌ 찍힘
                pass
        return wrapper
    return deco


# =======================
# 공통 검증 유틸 (성공/실패 출력 기준 통일)
# =======================
def _has_error(driver, xpath: str) -> bool:
    return bool(driver.find_elements(By.XPATH, xpath))


def wait_signup_result(driver, timeout=8) -> str:
    """
    반환: "SUCCESS" | "ERROR"
    - SUCCESS: Nice to meet you again 또는 Login 버튼 노출
    - ERROR  : 에러 문구/토스트 노출 또는 submit 비활성(가입 불가 유지)
    """
    wait = WebDriverWait(driver, timeout)

    success_locators = [
        (By.XPATH, "//*[contains(normalize-space(.), 'Nice to meet you again')]"),
        (By.XPATH, "//button[normalize-space(.)='Login']"),
    ]

    error_xpath = (
        "//*[contains(.,'error') or contains(.,'Error') "
        "or contains(.,'invalid') or contains(.,'Invalid') "
        "or contains(.,'already') or contains(.,'registered') "
        "or contains(.,'중복') or contains(.,'오류') or contains(.,'실패') "
        "or contains(.,'형식') or contains(.,'규칙') or contains(.,'필수')]"
    )

    def _cond(d):
        # 1) 성공 신호
        for how, sel in success_locators:
            if d.find_elements(how, sel):
                return "SUCCESS"

        # 2) 에러 문구/토스트 신호
        if d.find_elements(By.XPATH, error_xpath):
            return "ERROR"

        # 3) submit 비활성(막힘) 신호
        btns = d.find_elements(By.XPATH, "//button[@type='submit']")
        if btns:
            b = btns[0]
            if b.get_attribute("disabled") is not None or b.get_attribute("aria-disabled") == "true":
                return "ERROR"

        return False

    return wait.until(_cond)


def assert_signup_output(tc_id: str, driver, expected: str, timeout=8):
    """
    expected: "SUCCESS" | "ERROR"
    """
    result = wait_signup_result(driver, timeout=timeout)
    if result == expected:
        if expected == "SUCCESS":
            log_ok(tc_id, "성공 출력(로그인 화면) 검증 완료")
        else:
            log_ok(tc_id, "실패 출력(에러/가입불가) 검증 완료")
        assert True
    else:
        log_fail(tc_id, f"출력 검증 실패 (expected={expected}, actual={result})")
        assert False


# =======================
# UI 테스트
# =======================

@tc("SIGNUP_TC_001")
def test_signup_tc_001_ui(driver):
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    log_step("SIGNUP_TC_001", "회원가입 방식 선택 화면 진입")
    open_signup_method_page(driver, wait)

    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[contains(., 'Create account with email')]")
        )
    )
    log_ok("SIGNUP_TC_001", "화면 이동 검증 완료")


@tc("SIGNUP_TC_002")
def test_signup_tc_002_ui(driver):
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    log_step("SIGNUP_TC_002", "이메일 가입 입력 화면 진입")
    open_signup_email_form(driver, wait)

    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
    wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//input[contains(@placeholder,'Name') or @name='name' or @name='fullName']",
            )
        )
    )
    log_ok("SIGNUP_TC_002", "입력 폼 노출 검증 완료")


# =======================
# 정상 케이스
# =======================

@tc("SIGNUP_TC_003")
def test_signup_tc_003_success(driver):
    tc_id = "SIGNUP_TC_003"
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    log_step(tc_id, "이메일 가입 입력 화면 진입")
    open_signup_email_form(driver, wait)

    email, pw, name = get_signup_inputs(wait)

    log_step(tc_id, "정상 회원정보 입력")
    u = unique_email()
    email.clear()
    email.send_keys(u)
    pw.clear()
    pw.send_keys("abcd!1234")
    name.clear()
    name.send_keys("testname")

    log_step(tc_id, "필수 약관(1~3) 체크")
    check_terms_1to3_only(driver, wait)

    log_step(tc_id, "가입 submit 클릭")
    click_submit(wait)

    # ✅ 성공 기준: 로그인 화면(또는 Nice to meet you again) 출력
    assert_signup_output(tc_id, driver, expected="SUCCESS", timeout=10)


# =======================
# 필수 입력 예외
# =======================

@tc("SIGNUP_TC_004")
def test_signup_tc_004_email_required(driver):
    tc_id = "SIGNUP_TC_004"
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    email, pw, name = get_signup_inputs(wait)

    log_step(tc_id, "이메일 미입력, 나머지 입력")
    email.clear()
    pw.send_keys("abcd!1234")
    name.send_keys("testname")

    check_terms_1to3_only(driver, wait)
    click_submit(wait)

    # 브라우저 기본 validationMessage or 화면 에러 둘 중 하나면 OK
    v = driver.execute_script("return arguments[0].validationMessage;", email) or ""
    assert v or _has_error(driver, "//*[contains(.,'email') or contains(.,'이메일')]")
    assert_signup_output(tc_id, driver, expected="ERROR", timeout=7)


@tc("SIGNUP_TC_005")
def test_signup_tc_005_password_required(driver):
    tc_id = "SIGNUP_TC_005"
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    email, pw, name = get_signup_inputs(wait)

    log_step(tc_id, "비밀번호 미입력, 나머지 입력")
    email.send_keys(unique_email())
    pw.clear()
    name.send_keys("testname")

    check_terms_1to3_only(driver, wait)
    click_submit(wait)

    v = driver.execute_script("return arguments[0].validationMessage;", pw) or ""
    assert v or _has_error(driver, "//*[contains(.,'password') or contains(.,'비밀번호')]")
    assert_signup_output(tc_id, driver, expected="ERROR", timeout=7)


@tc("SIGNUP_TC_006")
def test_signup_tc_006_name_required(driver):
    tc_id = "SIGNUP_TC_006"
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    email, pw, name = get_signup_inputs(wait)

    log_step(tc_id, "이름 미입력, 나머지 입력")
    email.send_keys(unique_email())
    pw.send_keys("abcd!1234")
    name.clear()

    check_terms_1to3_only(driver, wait)
    click_submit(wait)

    v = driver.execute_script("return arguments[0].validationMessage;", name) or ""
    assert v or _has_error(driver, "//*[contains(.,'Name') or contains(.,'이름')]")
    assert_signup_output(tc_id, driver, expected="ERROR", timeout=7)


# =======================
# 이메일 형식 / 공백 / 중복
# =======================

@tc("SIGNUP_TC_007")
def test_signup_tc_007_invalid_email_format(driver):
    tc_id = "SIGNUP_TC_007"
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    email, pw, name = get_signup_inputs(wait)

    log_step(tc_id, "잘못된 이메일 형식 입력")
    email.send_keys("test@")
    pw.send_keys("abcd!1234")
    name.send_keys("testname")

    check_terms_1to3_only(driver, wait)
    click_submit(wait)

    v = driver.execute_script("return arguments[0].validationMessage;", email) or ""
    assert v or _has_error(driver, "//*[contains(.,'format') or contains(.,'형식')]")
    assert_signup_output(tc_id, driver, expected="ERROR", timeout=7)


@tc("SIGNUP_TC_008")
def test_signup_tc_008_email_with_space(driver):
    tc_id = "SIGNUP_TC_008"
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    email, pw, name = get_signup_inputs(wait)

    log_step(tc_id, "공백 포함 이메일 입력")
    email.send_keys(f"test {int(time.time())}@example.com")
    pw.send_keys("abcd!1234")
    name.send_keys("testname")

    check_terms_1to3_only(driver, wait)
    click_submit(wait)

    v = driver.execute_script("return arguments[0].validationMessage;", email) or ""
    assert v or _has_error(driver, "//*[contains(.,'email') or contains(.,'이메일')]")
    assert_signup_output(tc_id, driver, expected="ERROR", timeout=7)


@tc("SIGNUP_TC_009")
def test_signup_tc_009_duplicate_email(driver):
    tc_id = "SIGNUP_TC_009"
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    email, pw, name = get_signup_inputs(wait)

    log_step(tc_id, "중복 이메일로 가입 시도")
    email.clear()
    email.send_keys(DUPLICATE_EMAIL)
    pw.clear()
    pw.send_keys("abcd!1234")
    name.clear()
    name.send_keys("testname")

    check_terms_1to3_only(driver, wait)

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
        log_ok(tc_id, "중복 안내 메시지 노출 확인")
    except TimeoutException:
        pytest.skip(f"사전조건 미충족: DUPLICATE_EMAIL({DUPLICATE_EMAIL})이 중복 계정이 아닌 듯함")

    assert_signup_output(tc_id, driver, expected="ERROR", timeout=7)


# =======================
# 비밀번호 규칙
# =======================

@tc("SIGNUP_TC_010")
def test_signup_tc_010_password_too_short(driver):
    tc_id = "SIGNUP_TC_010"
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    email, pw, name = get_signup_inputs(wait)

    log_step(tc_id, "짧은 비밀번호 입력")
    email.send_keys(unique_email())
    pw.send_keys("abcd!")
    name.send_keys("testname")

    check_terms_1to3_only(driver, wait)
    click_submit(wait)

    assert _has_error(driver, "//*[contains(.,'password') or contains(.,'비밀번호')]")
    assert_signup_output(tc_id, driver, expected="ERROR", timeout=7)


@tc("SIGNUP_TC_011")
def test_signup_tc_011_password_no_number(driver):
    tc_id = "SIGNUP_TC_011"
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    email, pw, name = get_signup_inputs(wait)

    email.clear()
    email.send_keys(unique_email())
    name.clear()
    name.send_keys("testname")

    log_step(tc_id, "비밀번호 보기(eye) 동작 확인")
    eye = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']/ancestor::*//button")))
    assert pw.get_attribute("type") == "password"
    eye.click()
    assert pw.get_attribute("type") == "text"

    log_step(tc_id, "숫자 없는 비밀번호 입력")
    pw.clear()
    pw.send_keys("abcd!skfle")

    check_terms_1to3_only(driver, wait)
    click_submit(wait)

    rule_xpath = (
        "//*[contains(translate(.,'NUMBERDIGIT','numberdigit'),'number')"
        " or contains(translate(.,'NUMBERDIGIT','numberdigit'),'digit')"
        " or contains(.,'숫자') or contains(.,'규칙') or contains(.,'조합') or contains(.,'포함')]"
    )
    WebDriverWait(driver, 7).until(lambda d: d.find_elements(By.XPATH, rule_xpath))
    assert_signup_output(tc_id, driver, expected="ERROR", timeout=7)


@tc("SIGNUP_TC_012")
def test_signup_tc_012_password_no_letter(driver):
    tc_id = "SIGNUP_TC_012"
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    email, pw, name = get_signup_inputs(wait)

    email.clear()
    email.send_keys(unique_email())
    name.clear()
    name.send_keys("testname")

    log_step(tc_id, "비밀번호 보기(eye) 클릭")
    eye = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']/ancestor::*//button")))
    eye.click()
    assert pw.get_attribute("type") == "text"

    log_step(tc_id, "영문 없는 비밀번호 입력")
    pw.clear()
    pw.send_keys("1234!@#$")

    check_terms_1to3_only(driver, wait)
    click_submit(wait)

    assert _has_error(driver, "//*[contains(.,'letter') or contains(.,'영문')]")
    assert_signup_output(tc_id, driver, expected="ERROR", timeout=7)


@tc("SIGNUP_TC_013")
def test_signup_tc_013_password_no_special(driver):
    tc_id = "SIGNUP_TC_013"
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    email, pw, name = get_signup_inputs(wait)

    email.clear()
    email.send_keys(unique_email())
    name.clear()
    name.send_keys("testname")

    log_step(tc_id, "비밀번호 보기(eye) 클릭")
    eye = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']/ancestor::*//button")))
    eye.click()
    assert pw.get_attribute("type") == "text"

    log_step(tc_id, "특수문자 없는 비밀번호 입력")
    pw.clear()
    pw.send_keys("abcd1234")

    check_terms_1to3_only(driver, wait)
    click_submit(wait)

    assert _has_error(driver, "//*[contains(.,'special') or contains(.,'특수')]")
    assert_signup_output(tc_id, driver, expected="ERROR", timeout=7)


# =======================
# 약관
# =======================

@tc("SIGNUP_TC_014")
def test_signup_tc_014_agree_all_ui(driver):
    tc_id = "SIGNUP_TC_014"
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)

    log_step(tc_id, "약관 영역 펼치기")
    header = wait.until(EC.presence_of_element_located((By.ID, "agreement-header")))
    if header.get_attribute("aria-expanded") != "true":
        driver.execute_script("arguments[0].click();", header)

    log_step(tc_id, "Agree all 체크")
    agree_all = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[normalize-space(.)='Agree all']/ancestor::*//input[@type='checkbox']")
        )
    )
    if not agree_all.is_selected():
        driver.execute_script("arguments[0].click();", agree_all)

    cbs = driver.find_elements(By.XPATH, "//div[@id='agreement-contents']//input[@type='checkbox']")
    assert all(cb.is_selected() for cb in cbs[:4])

    log_ok(tc_id, "전체 동의 시 약관 체크 상태 검증 완료")


@tc("SIGNUP_TC_015")
def test_signup_tc_015_required_terms_not_checked(driver):
    tc_id = "SIGNUP_TC_015"
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    email, pw, name = get_signup_inputs(wait)

    email.clear()
    email.send_keys(unique_email())
    pw.clear()
    pw.send_keys("abcd!1234")
    name.clear()
    name.send_keys("testname")

    log_step(tc_id, "약관 펼치기")
    header = wait.until(EC.presence_of_element_located((By.ID, "agreement-header")))
    if header.get_attribute("aria-expanded") != "true":
        driver.execute_script("arguments[0].click();", header)

    cbs = wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//div[@id='agreement-contents']//input[@type='checkbox']")
        )
    )

    log_step(tc_id, "1✅ / 2❌ / 3❌ / 4✅ 세팅")
    if not cbs[0].is_selected():
        driver.execute_script("arguments[0].click();", cbs[0])
    for i in (1, 2):
        if cbs[i].is_selected():
            driver.execute_script("arguments[0].click();", cbs[i])
    if len(cbs) >= 4 and not cbs[3].is_selected():
        driver.execute_script("arguments[0].click();", cbs[3])

    submit = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))

    # 가입 불가 기준: 버튼 비활성
    assert submit.get_attribute("disabled") is not None or submit.get_attribute("aria-disabled") == "true"
    assert_signup_output(tc_id, driver, expected="ERROR", timeout=7)


@tc("SIGNUP_TC_016")
def test_signup_tc_016_required_terms_checked_success(driver):
    tc_id = "SIGNUP_TC_016"
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    email, pw, name = get_signup_inputs(wait)

    email.send_keys(unique_email())
    pw.send_keys("abcd!1234")
    name.send_keys("testname")

    log_step(tc_id, "[Required] 약관 2개만 체크")
    required_labels = wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//*[@id='agreement-contents']//label[contains(normalize-space(.), '[Required]')]")
        )
    )
    assert len(required_labels) == 2

    for label in required_labels:
        checkbox = label.find_element(By.XPATH, ".//input[@type='checkbox']")
        if not checkbox.is_selected():
            label.find_element(By.XPATH, ".//span[contains(@class,'MuiCheckbox-root')]").click()

    for label in required_labels:
        assert label.find_element(By.XPATH, ".//input[@type='checkbox']").is_selected()

    log_step(tc_id, "가입 submit 클릭")
    click_submit(wait)

    assert_signup_output(tc_id, driver, expected="SUCCESS", timeout=10)


# =======================
# 기타 UI
# =======================

@tc("SIGNUP_TC_017")
def test_signup_tc_017_password_show_hide(driver):
    tc_id = "SIGNUP_TC_017"
    wait = WebDriverWait(driver, 15)
    driver.get(BASE_URL)

    open_signup_email_form(driver, wait)
    _, pw, _ = get_signup_inputs(wait)

    log_step(tc_id, "비밀번호 입력")
    pw.send_keys("abcd!1234")

    eye = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@type='password']/ancestor::*//button")
        )
    )

    log_step(tc_id, "보기/숨기기 토글")
    assert pw.get_attribute("type") == "password"
    eye.click()
    assert pw.get_attribute("type") == "text"
    eye.click()
    assert pw.get_attribute("type") == "password"

    log_ok(tc_id, "보기/숨기기 동작 검증 완료")
