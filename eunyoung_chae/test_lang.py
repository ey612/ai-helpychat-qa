
# from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver


# 크롬 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# ================ 테스트 정보 ======================

# url = 'https://qaproject.elice.io/ai-helpy-chat'
# 아이디   : qa3team06@elicer.com
# 비밀번호 : 20qareset25elice!
WAIT_TIMEOUT = 5                # 요소 로드 대기 시간 (초)
# =================================================


# 드라이버 생성
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.implicitly_wait(WAIT_TIMEOUT)
wait = WebDriverWait(driver, WAIT_TIMEOUT)


# 사이트 접속
driver.get("https://qaproject.elice.io/ai-helpy-chat")
time.sleep(3)
print('✔️ 사이트 접속 완료')

# 로그인
print('== ID 입력 중 ==')
login_email = driver.find_element(By.CSS_SELECTOR, '[name="loginId"]')
login_email.send_keys("qa3team06@elicer.com")
print('✔️ ID 입력 완료 ')

print('== 비밀 번호 입력 중 ==')
login_pw = driver.find_element(By.CSS_SELECTOR, '[name="password"]')
login_pw.send_keys('20qareset25elice!')
print('== 비밀번호 입력 완료 ==')

print('== 로그인 버튼 클릭 중 ==')
login_btn = driver.find_element(By.ID, ':r3:').click()
print('✔️ 로그인 버튼 클릭 완료')

print("== 페이지 이동 확인 중 ==")
time.sleep(2)
print("✔️ 페이지 이동 확인 ==")

# [LANG_TC_001] 프로필 메뉴에서 [언어 설정] 클릭 시, 지원되는 언어 목록이 정상적으로 표시되는지 확인


# 사용자 아이콘 클릭
print('== 사용자 아이콘 클릭 중 ==')
personl_con = driver.find_element(By.CSS_SELECTOR, '[data-testid="PersonIcon"]')
personl_con.click()
print('✔️ 사용자 아이콘 클릭 완료')

# wait

print('== 언어 설정 클릭 중 ==')
language_setting = driver.find_element(By.XPATH, "//span[text()='언어 설정']")
language_setting.click()
print('✔️ 언어 설정 클릭 완료')

# 드롭다운 메뉴 뜰 때까지 대기
wait

# 드롭다운 메뉴 확인
expected_languages = [
    'American English',
    '한국어(대한민국)',
    'ไทย (ไทย)',
    '日本語 (日本)'
]

language_time_xpath_template = "//p[text()='{}']"

test_passed = True
for language in expected_languages:
    current_locator = (By.XPATH, language_time_xpath_template.format(language))
    
    try:
        driver.find_element(*current_locator)
        print(f" ✔️ [성공] '{language}' 항목이 확인 되었습니다.")
    except NoSuchElementException:
        print(f"❎ [실패] '{language}' 항목을 찾을 수 없습니다.")
        test_passed = False
