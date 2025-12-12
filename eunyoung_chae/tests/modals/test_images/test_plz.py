
# from selenium import webdriver
import os
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


# [IMG-MDL_TC_001] 업로드된 이미지 내용에 대한 질문 시 정확하게 답변하는지 확인

# [+] 버튼 누르기
print("== [+] 버튼 클릭하는 중 ==")
plus_icon = driver.find_element(By.CSS_SELECTOR, '[data-testid="plusIcon"]')
plus_icon.click()
print("== [+] 버튼 클릭 완료 ==")
time.sleep(3)

# 파일 업로드 버튼 클릭
print("== 파일 업로드 버튼 클릭하는 중 ==")
upload_file_btn = driver.find_element(By.XPATH, "//span[text()='파일 업로드']")
upload_file_btn.click()
print("== 파일 업로드 버튼 클릭 완료 ==")
time.sleep(5) 


try:
    # 파일 경로 지정
    relative_file_path = '../../data/images/elice.png'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    combined_path = os.path.join(current_dir, relative_file_path)
    file_path = os.path.abspath(combined_path)
    print(f"계산된 파일 경로: {file_path}")
    
    
    # 파일명만 추출
    file_name = os.path.basename(file_path)
    print(f"파일명: {file_name}")
    
    # 파일 존재 여부 확인
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
    print(f"파일 존재 확인 완료. 파일 크기: {os.path.getsize(file_path)}bytes")

    
    # 파일 탐색기에서 파일 업로드
    print("== 파일 탐색기로 파일 업로드 하는 중 ==")
    file_input_element = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
    file_input_element.send_keys(file_path)
    print("== 파일 input에 경로 전송 완료 ==")
    
    # 파일 업로드 완료 대기 중
    print(f"== '{file_name}' 이미지 업로드 완료 대기 중 ==")
    image_privew = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f'img[alt="{file_name}"]'))
    )
    print(f"== '{file_name}' 이미지 미리보기 확인 완료 ==")

    # 추가 안정화 대기
    print("== 추가 안정화 대기 (5초) ==")
    time.sleep(3)    
    
    print("== 파일 업로드 완료 ==")
    
except FileNotFoundError as e :
    print(f"❌ 파일 경로 오류: {e}")
except Exception as e :
    print(f"❌ 업로드 실패 오류: {e}")



print("==질문 입력 중==")
question_input = driver.find_element(By.NAME, 'input')
question_input.send_keys('총 몇명의 사람이 있나요? 파란색 튜튜를 입은 사람은 몇 명인가요? 주황색 옷을 입은 사람을 묘사해주세요.')
print('== 질문 입력 완료 ==')
time.sleep(15)

    
try :
    print('== 보내기 버튼 클릭하는 중 ==')
    send_btn_locator =(By.CSS_SELECTOR, '[aria-label="보내기"]')
    wait.until(EC.element_to_be_clickable(send_btn_locator))
    send_btn = driver.find_element(*send_btn_locator)
    send_btn.click()
    time.sleep(30)
    print('== 보내기 버튼 클릭 완료 ==')

except Exception as e :
    print(f'오류 떴어요 {e}')
    

# 적절한 대답이 오는지 확인
response_container = driver.find_element(By.CLASS_NAME, "elice-aichat__markdown")
response_text = response_container.text
print(response_text)

# assert "튜튜" in response_text, "'튜플' 단어 미포함"
# assert "튜튜" in response_text, "'튜플' 단어 미포함"
# assert "야외" in response_text, "'야외' 단어 미포함"
# assert "점프" in response_text, "'점프' 단어 미포함"
# assert "단체" in response_text, "'단체' 단어 미포함"



# # [IMG-MDL_TC_00 ]

# # [+] 버튼 누르기
# print("== [+] 버튼 클릭하는 중 ==")
# plus_icon = driver.find_element(By.CSS_SELECTOR, '[data-testid="plusIcon"]')
# plus_icon.click()
# print("== [+] 버튼 클릭 완료 ==")
# time.sleep(3)

# # 파일 업로드 버튼 클릭
# print("== 파일 업로드 버튼 클릭하는 중 ==")
# upload_file_btn = driver.find_element(By.XPATH, "//span[text()='파일 업로드']")
# upload_file_btn.click()
# print("== 파일 업로드 버튼 클릭 완료 ==")
# time.sleep(5) 


# try:
#     # 파일 경로 지정
#     relative_file_path = '../../data/wrong_image.png'
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     combined_path = os.path.join(current_dir, relative_file_path)
#     file_path = os.path.abspath(combined_path)
#     print(f"계산된 파일 경로: {file_path}")
    
    
#     # 파일명만 추출
#     file_name = os.path.basename(file_path)
#     print(f"파일명: {file_name}")
    
#     # 파일 존재 여부 확인
#     if not os.path.exists(file_path):
#         raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
#     print(f"파일 존재 확인 완료. 파일 크기: {os.path.getsize(file_path)}bytes")

    
#     # 파일 탐색기에서 파일 업로드
#     print("== 파일 탐색기로 파일 업로드 하는 중 ==")
#     file_input_element = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
#     file_input_element.send_keys(file_path)
#     print("== 파일 input에 경로 전송 완료 ==")
    
#     # 파일 업로드 완료 대기 중
#     print(f"== '{file_name}' 이미지 업로드 완료 대기 중 ==")
#     image_privew = wait.until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, f'img[alt="{file_name}"]'))
#     )
#     print(f"== '{file_name}' 이미지 미리보기 확인 완료 ==")
    
#     # 추가 안정화 대기
#     print("== 추가 안정화 대기 (5초) ==")
#     time.sleep(5)    
    
#     print("== 파일 업로드 완료 ==")
    
# except FileNotFoundError as e :
#     print(f"❌ 파일 경로 오류: {e}")
# except Exception as e :
#     print(f"❌ 업로드 실패 오류: {e}")

# print("==질문 입력 중==")
# question_input = driver.find_element(By.NAME, 'input')
# question_input.send_keys('총 몇명의 사람이 있나요? 파란색 튜튜를 입은 사람은 몇 명인가요? 주황색 옷을 입은 사람을 묘사해주세요.')
# print('== 질문 입력 완료 ==')
# time.sleep(15)
    
# try :
#     print('== 보내기 버튼 클릭하는 중 ==')
#     send_btn_locator =(By.CSS_SELECTOR, '[aria-label="보내기"]')
#     wait.until(EC.element_to_be_clickable(send_btn_locator))
#     send_btn = driver.find_element(*send_btn_locator)
#     send_btn.click()
#     time.sleep(30)
#     print('== 보내기 버튼 클릭 완료 ==')

# except Exception as e :
#     print(f'오류 떴어요 {e}')
    

# # 적절한 대답이 오는지 확인
# response_container = driver.find_element(By.CLASS_NAME, "elice-aichat__markdown")
# response_text = response_container.text
# print(response_text)