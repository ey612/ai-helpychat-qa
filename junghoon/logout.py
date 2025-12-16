from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def logout(driver, timeout: int = 10):
    wait = WebDriverWait(driver, timeout)

    # 1️⃣ 우측 상단 아바타(프로필) 버튼 클릭
    avatar_btn = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "button.MuiAvatar-root.MuiAvatar-circular"  # 필요 시 css 클래스 줄여도 됨
        ))
    )
    avatar_btn.click()
    print("👤 아바타 버튼 클릭 (로그아웃 메뉴 열기)")

    # 2️⃣ 드롭다운에서 '로그아웃' 메뉴 클릭
    logout_btn = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//*[text()='로그아웃']"
        ))
    )
    logout_btn.click()
    print("🚪 '로그아웃' 버튼 클릭 완료")

    # 3️⃣ (선택) 로그아웃 완료 확인
    # 예: 로그인 페이지로 이동했는지, 특정 요소가 보이는지 등
    # 이 부분은 서비스 구조에 맞게 커스터마이징 가능
    time.sleep(1)  # 간단히 1초 정도 대기