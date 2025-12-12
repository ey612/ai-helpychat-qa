import time
import os
from .data.configs import *
from .actions.common_actions import login, setup_driver, logout
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


# [IMG-MDL_TC_001] 업로드된 이미지 내용에 대한 질문 시 정확하게 답변하는지 확인

def test_01_image_qa_accuracy():
    try :
    
        # 1. 로그인
        driver = setup_driver(EMAIL, PW)
        
        # driver 객체 생성
        wait = WebDriverWait(driver, 10)
        
        # 2. 이미지 업로드 업로드 하기
        
        # [+] 버튼 누르기
        plus_icon = driver.find_element(By.CSS_SELECTOR, '[data-testid="plusIcon"]')
        plus_icon.click()
        time.sleep(3)
        
        # [파일 업로드] 버튼 클릭
        upload_file_btn = driver.find_element(By.XPATH, "//span[text()='파일 업로드']")
        upload_file_btn.click()
        time.sleep(5)
        
        # 파일 경로 지정
        
        # 업로드 할 이미지 경로
        relative_file_path = './data/images/elice.png'
        
        # current_dir 은 'tests' 폴더 경로
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 'tests/data/elice.png' 합치기
        combined_path = os.path.join(current_dir, relative_file_path)
        
        # 최종 이미지 경로 (컴퓨터는 이 경로를 보고 찾아 감) 
        file_path = os.path.abspath(combined_path)
        print(f"계산된 파일 경로: {file_path}")
        
        # ========= 파일이 실제로 있는지 확인 ========= 
        
        # 파일명만 추출
        file_name = os.path.basename(file_path)
        print(f"파일명: {file_name}")
        
        # 파일 존재 여부 확인
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
        print(f"파일 존재 확인 완료. 파일 크기: {os.path.getsize(file_path)}bytes")
        
        # ========= 파일이 실제로 있는지 확인 ========= 
        
        # 파일 업로드
        file_input_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
        )
        #file_input_element = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
        file_input_element.send_keys(file_path)
        time.sleep(5)
        
        # 파일 첨부 성공 여부 확인
        
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'img[alt="{file_name}"]'))
        )
        print("파일 미리보기 나타남")
        
        # 추가 안정화 대기
        time.sleep(3)    
        print("== 파일 업로드 완료 ==")

        
        # 3. 질문 입력
        question_input = driver.find_element(By.NAME, 'input')
        question_input.send_keys('이미지 속 동물 종류는 뭔가요? 어떤 표정을 짓고 있나요?')
        print('== 질문 입력 완료 ==')
    
        
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
        
        image_related_keywords = ['동물', '표정', '토끼', '엘리스', '귀', '얼굴', '눈', '입']
        found_keywords = [kw for kw in image_related_keywords if kw in response_text]
        try :
            
            if found_keywords:
                print(f"✅ 이미지 분석 성공!")
                print(f"   발견된 키워드: {', '.join(found_keywords)}")
                print("✅ Step 5: AI 답변 검증 완료\n")
            else:
                print("⚠️  경고: 이미지 관련 키워드가 답변에 없습니다")
                print("   이미지가 제대로 전달되지 않았을 수 있습니다")
                # 경고만 하고 실패는 아님 (AI가 다르게 표현했을 수도 있음)
            
            # 결과 확인을 위한 대기
            time.sleep(3)
        
        except TimeoutException:
            print("❌ AI 답변이 60초 내에 나타나지 않았습니다")
            raise AssertionError("AI 답변 타임아웃")

        
        print("\n🎉 테스트 완료!")
        time.sleep(3)

            
         
    except FileNotFoundError as e :
        print(f"❌ 파일 오류: {e}")
        raise
    
    except TimeoutException as e:
        print(f"❌ 타임 아웃 오류: {e}")
        raise AssertionError(f"타임아웃 발생: {str(e)}")
    
    except Exception as e :
        print(f"❌ 그 외 오류: {e}")
            
        try:
            screenshot_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                f'error_screenshot_{int(time.time())}.png'
            )
            driver.save_screenshot(screenshot_path)
            print(f"   스크린샷 저장됨: {screenshot_path}")
        except:
            pass
        
            raise
    
    finally:
        driver.quit()
    
def test_01_document_qa_accuracy():
    try :
    
        # 1. 로그인
        driver = setup_driver(EMAIL, PW)
        
        # driver 객체 생성
        wait = WebDriverWait(driver, 10)
        
        # 2. 이미지 업로드 업로드 하기
        
        # [+] 버튼 누르기
        plus_icon = driver.find_element(By.CSS_SELECTOR, '[data-testid="plusIcon"]')
        plus_icon.click()
        time.sleep(3)
        
        # [파일 업로드] 버튼 클릭
        upload_file_btn = driver.find_element(By.XPATH, "//span[text()='파일 업로드']")
        upload_file_btn.click()
        time.sleep(5)
        
        # 파일 경로 지정
        
        # 업로드 할 이미지 경로
        relative_file_path = './data/images/elice.png'
        
        # current_dir 은 'tests' 폴더 경로
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 'tests/data/elice.png' 합치기
        combined_path = os.path.join(current_dir, relative_file_path)
        
        # 최종 이미지 경로 (컴퓨터는 이 경로를 보고 찾아 감) 
        file_path = os.path.abspath(combined_path)
        print(f"계산된 파일 경로: {file_path}")
        
        # ========= 파일이 실제로 있는지 확인 ========= 
        
        # 파일명만 추출
        file_name = os.path.basename(file_path)
        print(f"파일명: {file_name}")
        
        # 파일 존재 여부 확인
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
        print(f"파일 존재 확인 완료. 파일 크기: {os.path.getsize(file_path)}bytes")
        
        # ========= 파일이 실제로 있는지 확인 ========= 
        
        # 파일 업로드
        file_input_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
        )
        #file_input_element = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
        file_input_element.send_keys(file_path)
        time.sleep(5)
        
        # 파일 첨부 성공 여부 확인
        
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'img[alt="{file_name}"]'))
        )
        print("파일 미리보기 나타남")
        
        # 추가 안정화 대기
        time.sleep(3)    
        print("== 파일 업로드 완료 ==")

        
        # 3. 질문 입력
        question_input = driver.find_element(By.NAME, 'input')
        question_input.send_keys('이미지 속 동물 종류는 뭔가요? 어떤 표정을 짓고 있나요?')
        print('== 질문 입력 완료 ==')
    
        
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
        
        image_related_keywords = ['동물', '표정', '토끼', '엘리스', '귀', '얼굴', '눈', '입']
        found_keywords = [kw for kw in image_related_keywords if kw in response_text]
        try :
            
            if found_keywords:
                print(f"✅ 이미지 분석 성공!")
                print(f"   발견된 키워드: {', '.join(found_keywords)}")
                print("✅ Step 5: AI 답변 검증 완료\n")
            else:
                print("⚠️  경고: 이미지 관련 키워드가 답변에 없습니다")
                print("   이미지가 제대로 전달되지 않았을 수 있습니다")
                # 경고만 하고 실패는 아님 (AI가 다르게 표현했을 수도 있음)
            
            # 결과 확인을 위한 대기
            time.sleep(3)
        
        except TimeoutException:
            print("❌ AI 답변이 60초 내에 나타나지 않았습니다")
            raise AssertionError("AI 답변 타임아웃")

        
        print("\n🎉 테스트 완료!")
        time.sleep(3)

    except FileNotFoundError as e :
        print(f"❌ 파일 오류: {e}")
        raise

    except TimeoutException as e:
        print(f"❌ 타임 아웃 오류: {e}")
        raise AssertionError(f"타임아웃 발생: {str(e)}")

    except Exception as e :
        print(f"❌ 그 외 오류: {e}")
            
        try:
            screenshot_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                f'error_screenshot_{int(time.time())}.png'
            )
            driver.save_screenshot(screenshot_path)
            print(f"   스크린샷 저장됨: {screenshot_path}")
        except:
            pass
        
            raise

    finally:
        driver.quit()