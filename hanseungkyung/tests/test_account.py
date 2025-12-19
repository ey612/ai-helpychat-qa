# -*- coding: utf-8 -*-
import os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ===== ENV =====
EMAIL = os.getenv("ELICE_QA_EMAIL", "qa3team0601@elicer.com")
PASSWORD = os.getenv("ELICE_QA_PW", "team06cheerup!")
HELPY_URL = os.getenv("HELPY_URL", "https://qaproject.elice.io/ai-helpy-chat")
NEW_NAME = os.getenv("ELICE_NEW_NAME", "team06_test2")


# ===== LOG =====
def step(msg): print(f"▶ {msg}")
def ok(msg):   print(f"✅ {msg}")
def ng(msg):   print(f"❌ {msg}")


# ===== SELENIUM UTILS =====
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

def js_click(d, el):
    d.execute_script("arguments[0].click();", el)

def force_click(d, by, val, t=15, desc="element"):
    el = find(d, by, val, t=t, desc=desc)
    try:
        d.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        time.sleep(0.2)
    except Exception:
        pass
    try:
        el.click()
    except Exception:
        js_click(d, el)
    return el

def body_has_any(d, texts):
    body = d.find_element(By.TAG_NAME, "body").text
    return any(x in body for x in texts)


# ===== DRIVER =====
def build_driver():
    opt = Options()
    opt.add_argument("--start-maximized")
    opt.add_argument("--disable-gpu")
    d = webdriver.Chrome(options=opt)
    d.implicitly_wait(0)
    return d


# ===== FLOWS =====
def login(d):
    d.get(HELPY_URL)

    visible(d, By.XPATH, "//input[@type='email' or contains(@name,'email') or contains(@id,'email')]",
            t=20, desc="email").send_keys(EMAIL)
    visible(d, By.XPATH, "//input[@type='password' or contains(@name,'password') or contains(@id,'password')]",
            t=20, desc="password").send_keys(PASSWORD)

    force_click(d, By.XPATH, "//button[@type='submit' or contains(.,'로그인') or @aria-label='로그인']",
                t=25, desc="login button")
    ok("로그인 버튼 클릭 완료")

    # 로그인 성공 판단(간단+튼튼)
    W(d, 25).until(lambda _d: _d.current_url != HELPY_URL or body_has_any(_d, ["로그아웃", "계정", "설정"]))
    ok("헬프쳇 접속/로그인 완료")


def go_account_management(d):
    # 프로필(아바타) 클릭
    force_click(
        d, By.XPATH,
        "//*[@data-testid='PersonIcon' or @data-testid='AccountCircleIcon' or contains(@class,'MuiAvatar') or contains(@class,'MuiAvatar-root')]",
        t=25, desc="profile/avatar"
    )
    ok("프로필 아이콘 클릭 완료")

    # 계정관리/설정 진입
    force_click(
        d, By.XPATH,
        "//*[self::a or self::button or self::li][contains(.,'계정') or contains(.,'설정') or contains(.,'Account')]",
        t=20, desc="account menu"
    )
    ok("계정관리(또는 설정) 메뉴 클릭 완료")


def edit_name_and_save(d, new_name: str):
    # ✅ 핵심 수정: 연필(button) 말고, 연필 포함 컨테이너(div)를 클릭
    force_click(
        d, By.XPATH,
        "//tr[.//td[normalize-space()='이름']]//div[contains(@class,'account--shared--editable-transition')]",
        t=20, desc="name editable container"
    )
    ok("이름 영역 클릭 완료(연필 포함 컨테이너)")

    # input 등장
    name_input = visible(d, By.XPATH, "//tr[.//td[normalize-space()='이름']]//input", t=15, desc="name input")
    name_input.clear()
    name_input.send_keys(new_name)
    ok(f"이름 입력 완료: {new_name}")

    # 저장 버튼(있으면 클릭)
    # (저장 버튼이 없고 blur/enter 저장인 경우도 있어서, 우선 버튼 시도 후 없으면 blur로 처리)
    try:
        force_click(
            d, By.XPATH,
            "//tr[.//td[normalize-space()='이름']]//button[contains(.,'저장') or contains(.,'완료') or contains(.,'확인') or @type='submit']",
            t=3, desc="name save button(in row)"
        )
        ok("이름 저장 버튼 클릭 완료")
    except Exception:
        # blur로 저장 유도
        d.execute_script("arguments[0].blur();", name_input)
        ok("저장 버튼 미확인 → blur로 저장 유도 완료")

    # 반영 확인: 텍스트로 돌아왔는지 확인
    W(d, 15).until(lambda _d: _d.find_element(By.TAG_NAME, "body") and new_name in _d.find_element(By.TAG_NAME, "body").text)
    ok(f"이름 변경 반영 확인 완료: {new_name}")


# ===== TEST =====
def test_account_management_flow():
    d = build_driver()
    try:
        step("브라우저 열림")
        step("헬프쳇 접속 후 로그인")
        login(d)

        step("계정관리 페이지 진입하기")
        go_account_management(d)
        ok("계정관리 페이지 진입 완료")

        step("이름 변경 기능 확인")
        edit_name_and_save(d, NEW_NAME)

        ok("계정관리(이름 변경) 플로우 완료")
    finally:
        pass  # 필요하면 d.quit()


if __name__ == "__main__":
    test_account_management_flow()
