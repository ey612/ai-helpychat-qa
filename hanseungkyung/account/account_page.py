# account/account_page.py
from selenium.webdriver.common.by import By


class AccountPage:
    # ===== Helpy Chat (qaproject.elice.io) =====
    # 우측 상단 사람(아바타) 버튼: svg data-testid=PersonIcon 이 들어있음
    AVATAR_BTN = (
        By.XPATH,
        "//button[.//svg[@data-testid='PersonIcon'] "
        "or contains(@class,'MuiAvatar-root') "
        "or .//svg[contains(@data-testid,'Person')]]",
    )

    # 프로필 패널에서 '계정 관리' 클릭 (span 텍스트가 가장 안정적)
    ACCOUNT_MANAGEMENT_LINK = (
        By.XPATH,
        "//span[normalize-space()='계정 관리' or contains(normalize-space(),'계정 관리')]",
    )

    # ===== Elice Account (accounts.elice.io) =====
    # 계정관리 페이지 로딩 확인용 (기본정보/이름 입력창 등)
    READY = (
        By.XPATH,
        "//*[contains(normalize-space(),'기본 정보') or contains(normalize-space(),'계정 관리')]",
    )

    # 이름 수정(연필) 버튼: EditOutlinedIcon 사용
    NAME_EDIT_BTN = (
        By.XPATH,
        "//*[normalize-space()='이름']/ancestor::tr[1]//button"
        "[.//svg[@data-testid='EditOutlinedIcon'] or .//svg[contains(@data-testid,'Edit')]]",
    )

    # 이름 입력: 너 스샷에서 name='fullName' 으로 확정
    NAME_INPUT = (
        By.CSS_SELECTOR,
        "input[name='fullName']",
    )

    # 비밀번호 수정(연필) 버튼
    PASSWORD_EDIT_BTN = (
        By.XPATH,
        "//*[normalize-space()='비밀번호']/ancestor::tr[1]//button"
        "[.//svg[@data-testid='EditOutlinedIcon'] or .//svg[contains(@data-testid,'Edit')]]",
    )

    # 기존 비밀번호 input (스샷에서 autocomplete='current-password')
    CURRENT_PW_INPUT = (
        By.CSS_SELECTOR,
        "input[autocomplete='current-password']",
    )

    # 새 비밀번호 input (보통 autocomplete='new-password')
    NEW_PW_INPUT = (
        By.CSS_SELECTOR,
        "input[autocomplete='new-password']",
    )

    # 완료 버튼
    DONE_BTN = (
        By.XPATH,
        "//button[normalize-space()='완료']",
    )

    # 저장 성공 토스트(스샷: Saved successfully.)
    SAVE_TOAST = (
        By.XPATH,
        "//*[contains(normalize-space(),'Saved successfully') or contains(normalize-space(),'저장')]",
    )

    # 프로모션 알림(마케팅) 토글: input name='marketing' (스샷 확정)
    PROMO_MARKETING = (
        By.CSS_SELECTOR,
        "input[name='marketing']",
    )
