# -*- coding: utf-8 -*-
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ===== 환경변수/기본값 =====
EMAIL = os.getenv("ELICE_QA_EMAIL", "qa3team0601@elicer.com")
PASSWORD = os.getenv("ELICE_QA_PW", "team06cheerup!")
HELPY_URL = os.getenv("HELPY_URL", "https://qaproject.elice.io/ai-helpy-chat")

ACCOUNTS_DOMAIN = "accounts.elice.io"
ACCOUNT_PATH = "/members/account"

# ===== 출력 =====
def step(msg: str):
    print(msg)

def ok(msg: str):
    print(f"✅ {msg}")

# ===== 드라이버 =====
def build_driver():
    opt = webdriver.ChromeOptions()
    opt.add_argument("--start-maximized")
    d = webdriver.Chrome(options=opt)
    d.set_page_load_timeout(30)
    return d

def w(d, t=15):
    return WebDriverWait(d, t)

# ===== Wait/Click 유틸 =====
def wait_present(d, by, val, t=15, desc="element"):
    try:
        return WebDriverWait(d, t).until(EC.presence_of_element_located((by, val)))
    except Exception as e:
        raise AssertionError(f"[FAIL] {desc} present 못찾음\n{by}={val}\nURL={d.current_url}\n{e}")

def wait_visible(d, by, val, t=15, desc="element"):
    try:
        return WebDriverWait(d, t).until(EC.visibility_of_element_located((by, val)))
    except Exception as e:
        raise AssertionError(f"[FAIL] {desc} visible 못찾음\n{by}={val}\nURL={d.current_url}\n{e}")

def wait_text_any(d, keywords, t=15):
    def _cond(_):
        src = d.page_source
        return any(k in src for k in keywords)
    WebDriverWait(d, t).until(_cond)

def js_click(d, el):
    d.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
    d.execute_script("arguments[0].click();", el)

def type_clear(el, text):
    el.click()
    el.send_keys(Keys.CONTROL, "a")
    el.send_keys(Keys.BACKSPACE)
    el.send_keys(text)

# ===== 1) 헬프쳇 접속/로그인 =====
def do_accounts_login_if_needed(d):
    # accounts 로그인 페이지일 때만 로그인 수행
    if ACCOUNTS_DOMAIN not in d.current_url:
        return

    email_in = wait_visible(d, By.CSS_SELECTOR, "input[type='email']", desc="email input")
    pw_in = wait_visible(d, By.CSS_SELECTOR, "input[type='password']", desc="password input")

    type_clear(email_in, EMAIL)
    type_clear(pw_in, PASSWORD)

    submit = wait_present(d, By.CSS_SELECTOR, "button[type='submit'], input[type='submit']", desc="submit button")
    js_click(d, submit)

def open_helpy_and_login(d):
    d.get(HELPY_URL)

    # 헬프쳇 접속 시 accounts로 리다이렉트 되면 로그인 처리
    if ACCOUNTS_DOMAIN in d.current_url:
        do_accounts_login_if_needed(d)
        w(d, 20).until(lambda _ : "qaproject.elice.io" in d.current_url)

# ===== 2) 프로필 패널 열기 (PersonIcon) =====
def open_profile_panel(d):
    btn = wait_present(
        d,
        By.XPATH,
        "//button[.//*[@data-testid='PersonIcon']]",
        desc="person icon button"
    )
    js_click(d, btn)

    # 패널 열림 확인: '계정 관리' 메뉴가 나타나는지로 판단
    wait_present(d, By.XPATH, "//span[normalize-space()='계정 관리']", desc="profile panel menu: 계정 관리")

# ===== 3) 계정관리 페이지 진입 (새 탭) =====
def go_account_management_from_profile(d):
    link = wait_present(
        d,
        By.XPATH,
        "//a[contains(@href,'accounts.elice.io') and .//span[normalize-space()='계정 관리']]",
        desc="'계정 관리' link"
    )
    js_click(d, link)

    w(d, 10).until(lambda _ : len(d.window_handles) >= 2)
    d.switch_to.window(d.window_handles[-1])

    w(d, 20).until(lambda _ : (ACCOUNTS_DOMAIN in d.current_url and ACCOUNT_PATH in d.current_url))
    ok(f"계정관리 페이지 진입 확인: {d.current_url}")


# =========================
# STEP1 테스트 (가이드 문구 그대로)
# =========================
def test_account_management_flow():
    d = build_driver()
    try:
        step("브라우저 열림")

        step("헬프쳇 접속 후 로그인")
        open_helpy_and_login(d)
        ok("헬프쳇 접속/로그인 완료")

        step("1.계정관리 페이지 진입하기")
        open_profile_panel(d)
        go_account_management_from_profile(d)
        ok("계정관리 페이지 진입 완료")

        
        # =========================
        # 2. 이름 변경 기능 확인
        # =========================
        step("2.이름 변경 기능이 정상 동작하는지 확인")

        NEW_NAME = os.getenv("ELICE_NEW_NAME", "team06_test")

        # 이름 행의 연필 버튼 클릭
        edit_btn = wait_present(
            d,
            By.XPATH,
            "//tr[.//td[normalize-space()='이름']]//button[.//*[@data-testid='EditOutlinedIcon']]",
            desc="이름 수정 연필 버튼"
        )
        js_click(d, edit_btn)
        ok("이름 수정 연필 클릭")

        # 이름 input
        name_input = wait_visible(
            d,
            By.XPATH,
            "//tr[.//td[normalize-space()='이름']]//input",
            desc="이름 입력창"
        )
        name_input.click()
        name_input.send_keys(Keys.CONTROL, "a")
        name_input.send_keys(Keys.BACKSPACE)
        name_input.send_keys(NEW_NAME)
        ok(f"이름 입력: {NEW_NAME}")

        # 완료 버튼
        done_btn = wait_present(
            d,
            By.XPATH,
            "//button[normalize-space()='완료']",
            desc="완료 버튼"
        )
        js_click(d, done_btn)
        ok("완료 버튼 클릭")

        # 성공 메시지 확인
        wait_text_any(d, ["저장", "성공", "변경", "완료"], t=15)
        ok("이름 변경 정상 처리 확인")
        
          
        # 비밀번호 행의 연필 버튼 클릭
        edit_btn = wait_present(
            d,
            By.XPATH,
            "//tr[.//td[normalize-space()='비밀번호']]//button[.//*[@data-testid='EditOutlinedIcon']]",
            desc="비밀번호 수정 연필 버튼"
        )
        js_click(d, edit_btn)
        ok("비밀번호 수정 연필 클릭")



































    finally:
        pass  # 브라우저 유지
        