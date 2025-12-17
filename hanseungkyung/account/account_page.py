# account/account_page.py
from selenium.webdriver.common.by import By


class AccountPage:
    # ✅ 사람 아이콘 버튼: 후보를 여러 개로 둠(안정)
    AVATAR_BTN_CANDIDATES = [
        # MUI Avatar 버튼(스샷에 확실히 존재)
        (By.CSS_SELECTOR, "button.MuiAvatar-root"),
        # 혹시 IconButton으로 감싸진 경우
        (By.CSS_SELECTOR, "button.MuiIconButton-root:has(svg)"),
        # data-testid가 있는 경우(있으면 가장 좋음)
        (By.XPATH, "//button[.//svg[@data-testid='PersonIcon']]"),
        (By.XPATH, "//*[@data-testid='PersonIcon']/ancestor::button[1]"),
    ]

    # 계정관리 메뉴
    ACCOUNT_MENU_CANDIDATES = [
        (By.XPATH, "//*[self::li or self::button or self::a][contains(.,'계정관리')]"),
        (By.XPATH, "//*[self::li or self::button or self::a][contains(.,'계정 관리')]"),
    ]

    # 공통 저장 버튼
    SAVE_BTN = (By.XPATH, "//button[contains(.,'저장')]")

    # 이름 변경
    NAME_CHANGE_BTN = (By.XPATH, "//*[contains(.,'이름 변경')]")
    NAME_INPUT = (By.XPATH, "//input[@name='name' or contains(@placeholder,'이름') or @type='text']")

    # 비밀번호 변경
    PASSWORD_CHANGE_BTN = (By.XPATH, "//*[contains(.,'비밀번호 변경')]")
    CURRENT_PW_INPUT = (By.XPATH, "(//input[@type='password'])[1]")
    NEW_PW_INPUT = (By.XPATH, "(//input[@type='password'])[2]")
    CONFIRM_PW_INPUT = (By.XPATH, "(//input[@type='password'])[3]")

    # 프로모션 알림 토글
    PROMOTION_TOGGLE = (By.XPATH, "//*[contains(.,'프로모션')]/following::*[@role='switch' or @type='checkbox'][1]")

    # 메시지
    TOAST = (By.XPATH, "//*[contains(.,'저장') or contains(.,'되었습니다')]")
    ERROR_MSG = (By.XPATH, "//*[contains(.,'강력') or contains(.,'8자') or contains(.,'특수문자')]")
