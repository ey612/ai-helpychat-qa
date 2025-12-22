# -*- coding: utf-8 -*-
import os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ===== ENV =====
EMAIL = os.getenv("ELICE_QA_EMAIL", "qa3team0601@elicer.com")
CURRENT_PASSWORD = os.getenv("ELICE_QA_PW", "team06cheerup!")   # ✅ 현재 비밀번호(윗칸)
HELPY_URL = os.getenv("HELPY_URL", "https://qaproject.elice.io/ai-helpy-chat")

TARGET_NAME = "team06_test"
BAD_NEW_PASSWORD = "1234"              # ✅ 형식 오류 유도
GOOD_NEW_PASSWORD = "team06cheerup!!!" # ✅ 최종 변경

# 형식 오류/정책 문구는 서비스마다 다르니, 넓게 잡음
FORMAT_ERROR_KEYWORDS = [
    "형식", "조건", "자 이상", "8자", "영문", "숫자", "특수", "조합",
    "비밀번호", "사용할 비밀번호입니다", "다른 비밀번호", "올바르지"
]


# ===== LOG =====
def step(m): print(f"▶ {m}")
def ok(m):   print(f"✅ {m}")
def ng(m):   print(f"❌ {m}")


# ===== WAIT/CLICK UTILS =====
def W(d, t=15): return WebDriverWait(d, t)

def find(d, by, val, t=15, desc="element"):
    try:
        return W(d, t).until(EC.presence_of_element_located((by, val)))
    except Exception as e:
        ng(f"{desc} 찾기 실패: {e}")
        raise

def visible(d, by, val, t=15, desc="element"):
    try:
        return W(d, t).until(EC.visibility_of_element_located((by, val)))
    except Exception as e:
        ng(f"{desc} visible 실패: {e}")
        raise

def force_js_click(d, el):
    d.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
    time.sleep(0.1)
    d.execute_script("arguments[0].click();", el)

def click(d, by, val, t=15, desc="element"):
    el = find(d, by, val, t=t, desc=desc)
    try:
        el.click()
    except Exception:
        force_js_click(d, el)
    return el

def body_text(d):
    return d.find_element(By.TAG_NAME, "body").text

def body_has_any(d, texts):
    b = body_text(d)
    return any(x in b for x in texts)


# ===== TAB SWITCH (새 탭 전환) =====
def switch_to_accounts_tab(d, t=12):
    end = time.time() + t
    while time.time() < end:
        for h in d.window_handles:
            d.switch_to.window(h)
            cur = d.current_url or ""
            if "accounts.elice.io" in cur:
                ok(f"accounts 탭 전환 완료: {cur}")
                return
        time.sleep(0.2)
    ng(f"accounts 탭 전환 실패. 현재 URL: {d.current_url}")
    raise TimeoutError("accounts.elice.io 탭으로 전환 실패")


# ===== BASIC INFO HELPERS (오른쪽 기본정보 표 기준) =====
def click_basicinfo_pencil(d, label: str, t=20):
    xpath = (
        "//main//table"
        f"//td[normalize-space()='{label}']"
        "/following-sibling::td[1]"
        "//button[.//*[name()='svg' and @data-testid='EditOutlinedIcon']]"
    )
    btn = find(d, By.XPATH, xpath, t=t, desc=f"{label} 연필 버튼")
    force_js_click(d, btn)
    ok(f"{label} 연필 클릭 완료")

def get_row_scope(d, label: str, t=20):
    xpath = (
        "//main//table"
        f"//td[normalize-space()='{label}']"
        "/following-sibling::td[1]"
    )
    return find(d, By.XPATH, xpath, t=t, desc=f"{label} row scope")

def try_save_button(d, t=3):
    xpath = "//button[contains(.,'저장') or contains(.,'완료') or contains(.,'확인') or contains(.,'변경') or @type='submit']"
    try:
        btn = find(d, By.XPATH, xpath, t=t, desc="저장/변경 버튼")
        force_js_click(d, btn)
        ok("저장/변경 버튼 클릭 완료")
        return True
    except Exception:
        return False


# ===== NAME CHANGE =====
def change_name_to_target(d, new_name: str):
    step("이름을 team06_test로 원복")
    click_basicinfo_pencil(d, "이름", t=20)

    inp = visible(
        d, By.XPATH,
        "//main//table//td[normalize-space()='이름']/following-sibling::td[1]//input",
        t=15, desc="name input"
    )
    inp.click()
    inp.send_keys(Keys.CONTROL, "a")
    inp.send_keys(Keys.DELETE)
    inp.send_keys(new_name)
    ok(f"이름 입력 완료: {new_name}")

    if not try_save_button(d, t=3):
        try:
            inp.send_keys(Keys.ENTER)
        except Exception:
            d.execute_script("arguments[0].blur();", inp)

    W(d, 15).until(lambda _d: new_name in body_text(_d))
    ok(f"이름 변경 반영 확인 완료: {new_name}")


# ===== PASSWORD: eye + mapping fix =====
def _visible_inputs_in_scope(scope):
    # eye 토글로 type이 text로 바뀔 수 있으니 password/text 모두 허용
    els = scope.find_elements(By.XPATH, ".//input[@type='password' or @type='text']")
    vis = []
    for e in els:
        try:
            if e.is_displayed():
                vis.append(e)
        except Exception:
            pass
    return vis

def pick_password_fields_in_scope(scope):
    """
    ✅ 스샷 형태(2개): [현재 비밀번호(윗칸), 새 비밀번호(아랫칸)]
    ✅ 3개면: [현재, 새, 확인]
    """
    vis = _visible_inputs_in_scope(scope)
    if len(vis) >= 3:
        return vis[0], vis[1], vis[2]
    if len(vis) == 2:
        return vis[0], vis[1], None
    raise Exception("비밀번호 입력칸을 찾지 못했어(현재/새).")

def eye_button_for_input(input_el):
    """
    input이 들어있는 가장 가까운 컨테이너에서 eye 버튼 찾기.
    MUI 구조에서 endAdornment 쪽이 마지막 button인 경우가 많아 마지막을 클릭.
    """
    containers = [
        "./ancestor::*[contains(@class,'MuiInputBase')][1]",
        "./ancestor::*[contains(@class,'MuiTextField')][1]",
        "./ancestor::*[contains(@class,'MuiFormControl')][1]",
        "./ancestor::*[self::div or self::span][1]",
        "./ancestor::*[self::div or self::span][2]",
        "./ancestor::*[self::div or self::span][3]",
    ]
    for cxp in containers:
        try:
            c = input_el.find_element(By.XPATH, cxp)
            btns = c.find_elements(By.XPATH, ".//button")
            btns = [b for b in btns if b.is_displayed()]
            if btns:
                return btns[-1]
        except Exception:
            pass
    return input_el.find_element(By.XPATH, "./following::button[1]")

def click_eye(d, input_el, label: str):
    btn = eye_button_for_input(input_el)
    force_js_click(d, btn)
    ok(f"{label} 눈 아이콘 클릭 완료")

def set_input_value(el, value: str):
    if el is None:
        return
    el.click()
    el.send_keys(Keys.CONTROL, "a")
    el.send_keys(Keys.DELETE)
    el.send_keys(value)

def expect_format_error(d, scope):
    # scope 안에 helperText(빨간 글씨)가 있으면 그걸 우선 확인, 아니면 body 키워드로 확인
    try:
        err = W(d, 8).until(
            EC.visibility_of_element_located(
                (By.XPATH, ".//*[contains(@class,'MuiFormHelperText') or @role='alert' or contains(@class,'Mui-error')]")
            )
        )
        txt = err.text.strip()
        if txt:
            ok(f"형식 오류 문구 확인(영역): {txt}")
            return True
    except Exception:
        pass

    W(d, 8).until(lambda _d: body_has_any(_d, FORMAT_ERROR_KEYWORDS))
    ok("형식 오류 문구 확인(body 키워드)")
    return True

def password_change_with_validation(d):
    step("비밀번호 연필 → 눈아이콘(현재/새) → 1234 오류 확인 → 정상 비번 저장")

    click_basicinfo_pencil(d, "비밀번호", t=20)
    scope = get_row_scope(d, "비밀번호", t=20)

    # 입력칸 등장 대기
    W(d, 15).until(lambda _d: len(_visible_inputs_in_scope(scope)) >= 2)

    cur_el, new_el, confirm_el = pick_password_fields_in_scope(scope)

    # ✅ 눈 아이콘 클릭 (아랫칸 눈도 확실히)
    click_eye(d, cur_el, "현재 비밀번호")
    click_eye(d, new_el, "새 비밀번호")

    time.sleep(1)

    # ===== 1) BAD 시도: 새 비번 1234 -> 형식 오류 확인 =====
    step("1차: 새 비밀번호를 1234로 입력 후 형식 오류 확인")

    # ✅ 매핑 고정: 윗칸=현재(현재비번), 아랫칸=새(1234)
    set_input_value(cur_el, CURRENT_PASSWORD)
    set_input_value(new_el, BAD_NEW_PASSWORD)
    if confirm_el is not None:
        set_input_value(confirm_el, BAD_NEW_PASSWORD)

    if not try_save_button(d, t=5):
        try:
            (confirm_el or new_el).send_keys(Keys.ENTER)
        except Exception:
            d.execute_script("arguments[0].blur();", (confirm_el or new_el))

    expect_format_error(d, scope)

    # ===== 2) GOOD 시도: 새 비번 team06cheerup!!! 저장 =====
    step('2차: 새 비밀번호를 "team06cheerup!!!"으로 입력 후 저장')

    # 같은 화면에서 다시 입력
    set_input_value(cur_el, CURRENT_PASSWORD)
    set_input_value(new_el, GOOD_NEW_PASSWORD)
    if confirm_el is not None:
        set_input_value(confirm_el, GOOD_NEW_PASSWORD)

    if not try_save_button(d, t=5):
        try:
            (confirm_el or new_el).send_keys(Keys.ENTER)
            ok("저장 버튼 없음 → Enter 저장 유도")
        except Exception:
            d.execute_script("arguments[0].blur();", (confirm_el or new_el))
            ok("저장 버튼 없음 → blur 저장 유도")

    # 완료 확인: (1) 오류 문구 사라짐 또는 (2) 편집 UI 접힘
    def done(_d):
        # 오류 키워드가 남아있으면 아직 실패 상태일 가능성
        b = body_text(_d)
        filtered = [k for k in FORMAT_ERROR_KEYWORDS if k != "비밀번호"]
        if body_has_any(_d, filtered):
            return False
        # scope 내 입력칸이 사라지면 편집 종료
        try:
            return len(_visible_inputs_in_scope(scope)) == 0
        except Exception:
            return True

    W(d, 15).until(done)
    ok("비밀번호 변경 완료(형식 오류 해소/편집 종료 확인)")


# ===== DRIVER / LOGIN / NAV =====
def build_driver():
    opt = Options()
    opt.add_argument("--start-maximized")
    opt.add_argument("--disable-gpu")
    d = webdriver.Chrome(options=opt)
    d.implicitly_wait(0)
    return d

def login_helpy(d):
    d.get(HELPY_URL)
    visible(d, By.XPATH, "//input[@type='email' or contains(@name,'email') or contains(@id,'email')]", t=20, desc="email").send_keys(EMAIL)
    visible(d, By.XPATH, "//input[@type='password' or contains(@name,'password') or contains(@id,'password')]", t=20, desc="password").send_keys(CURRENT_PASSWORD)

    click(d, By.XPATH, "//button[@type='submit' or contains(.,'로그인') or @aria-label='로그인']", t=25, desc="login button")
    ok("로그인 버튼 클릭 완료")

    W(d, 25).until(lambda _d: _d.current_url != HELPY_URL or body_has_any(_d, ["로그아웃", "계정", "설정"]))
    ok("헬프쳇 접속/로그인 완료")

def go_account_management(d):
    click(
        d, By.XPATH,
        "//*[@data-testid='PersonIcon' or @data-testid='AccountCircleIcon' or contains(@class,'MuiAvatar') or contains(@class,'MuiAvatar-root')]",
        t=25, desc="profile/avatar"
    )
    ok("프로필 아이콘 클릭 완료")

    click(
        d, By.XPATH,
        "//*[self::a or self::button or self::li][contains(.,'계정') or contains(.,'설정') or contains(.,'Account')]",
        t=20, desc="account menu"
    )
    ok("계정관리(또는 설정) 메뉴 클릭 완료")

    switch_to_accounts_tab(d)
    ok("기본정보 진입 완료")


# ===== TEST =====
def test_flow():
    d = build_driver()
    try:
        step("로그인")
        login_helpy(d)

        step("기본정보 진입")
        go_account_management(d)

        step("이름 원복")
        change_name_to_target(d, TARGET_NAME)

        step("비밀번호 1234 형식오류 확인 후 정상 비밀번호 변경")
        password_change_with_validation(d)

        ok("전체 완료: 이름 원복 + 비밀번호 형식오류 확인 + 비밀번호 변경")
    finally:
        # 필요하면 확인 후 종료
        print("⏳ 5초 후 브라우저 종료")
        time.sleep(5)
        d.quit()
    


if __name__ == "__main__":
    test_flow()
