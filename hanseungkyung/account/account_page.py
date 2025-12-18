# account/account_page.py
from selenium.webdriver.common.by import By


class AccountPage:
    # ===== 이름(연필) =====
    # '이름' 라벨이 있는 행에서만 연필(편집) 버튼 찾기
    NAME_EDIT_BTN = (
        By.XPATH,
        "//tr[.//th[normalize-space()='이름']]//button[.//svg[@data-testid='EditOutlinedIcon']]"
    )

    # 이름 입력창 (input name="fullname")
    NAME_INPUT = (By.CSS_SELECTOR, "input[name='fullname']")

    # '완료' 버튼
    SAVE_BTN = (By.XPATH, "//button[normalize-space()='완료']")

    # ===== 비밀번호(연필) =====
    PASSWORD_EDIT_BTN = (
        By.XPATH,
        "//tr[.//th[normalize-space()='비밀번호']]//button"
    )

    CURRENT_PW_INPUT = (By.CSS_SELECTOR, "input[name='password']")
    NEW_PW_INPUT = (By.CSS_SELECTOR, "input[name='newPassword']")

    # 눈 아이콘(토글) 버튼들
    EYE_BTNS = (By.CSS_SELECTOR, "button[aria-label='toggle password visibility']")

    # ===== 프로모션 =====
    PROMO_TOGGLE = (By.CSS_SELECTOR, "input[name='marketing']")
