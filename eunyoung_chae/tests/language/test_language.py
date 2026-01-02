import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from src.pages.login_page import LoginPage
from src.pages.main_page import GnbComponent
from src.config.config import EMAIL, PW


# [LANG_TC_001] 프로필 메뉴에서 언어 설정 클릭 시 지원 언어 목록이 표시되는지 확인
def test_001_language_menu_shows_supported_languages(driver):
    wait = WebDriverWait(driver, 10)
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)

    # 테스트 로직 실행

    # 1. 사용자 아이콘 클릭
    personl_icon = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="PersonIcon"]'))
    )
    personl_icon.click()
    print("✔️ 사용자 아이콘 클릭 완료")

    # 2. 언어 설정 클릭
    print("== 언어 설정 클릭 중 ==")
    language_setting = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='언어 설정']"))
    )
    language_setting.click()
    print("✔️ 언어 설정 클릭 완료")

    # 드롭다운 메뉴 확인
    expected_languages = [
        "American English",
        "한국어(대한민국)",
        "ไทย (ไทย)",
        "日本語 (日本)",
    ]

    language_time_xpath_template = "//p[text()='{}']"

    test_passed = True
    for language in expected_languages:
        current_locator = (By.XPATH, language_time_xpath_template.format(language))

        try:
            wait.until(
                EC.presence_of_element_located(current_locator)
            )
            print(f" ✔️ [성공] '{language}' 항목이 확인 되었습니다.")
        except TimeoutException:
            print(f"❎ [실패] '{language}' 항목을 찾을 수 없습니다.")
            test_passed = False
    assert test_passed, "모든 언어 항목이 드롭다운에 표시되지 않았습니다."


# [LANG_TC_002] 언어 변경 후 재로그인 시 선택한 언어 설정이 유지되는지 확인
def test_002_language_setting_persists_after_relogin(driver):
    VERIFICATION_TEXT = "Account Management"
    wait = WebDriverWait(driver, 10)
    
    try:
        # 로그인
        login_page = LoginPage(driver)
        login_page.login(PW, EMAIL)
    except Exception as e:
        assert False, f"로그인 실패: {e}"

    gnd_component = GnbComponent(driver)

    try:
        gnd_component.click_person_icon()
        
        wait.until(
            EC.visibility_of_element_located((By.XPATH, "//span[text()='언어 설정']"))
        )

        # 2. 언어 설정 클릭
        print("== 언어 설정 클릭 중 ==")
                
        language_setting = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='언어 설정']"))
        )
        language_setting.click()
        print("✔️ 언어 설정 클릭 완료")

        # 3. 언어 선택 (한국어 -> English)
        language_english = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//p[text()='American English']"))
        )
        language_english.click()
        print("✔️ 한국어 --> 영어로 변경 완료!")

        # 4. 언어 변경 확인 (검증)
        
        #  언어 변경이 반영된 UI 상태를 기다려.
        account_mgmt_element = wait.until(
            EC.visibility_of_element_located(gnd_component.locators["account_management"])
        )
        print(
            f"✅ 언어 변경 확인 성공: '{VERIFICATION_TEXT}' 텍스트가 화면에서 확인되었습니다."
        )

        # 5. 새로 고침
        driver.refresh()
        print("✔️ 페이지를 새로고침했습니다.")
        # 드롭다운이 보이지 않을 때까지 기다려
        wait.until(
            EC.invisibility_of_element_located(gnd_component.locators["account_management"])
        )

        # 7.로그아웃
        login_btn = gnd_component.logout()
        assert login_btn.is_displayed()
        
        # 로그인
        wait.until(
            EC.visibility_of_element_located(
                login_page.locators["login_button"]
            )
        )
        login_page.login(PW)
        
        wait.until(
            EC.invisibility_of_element_located(
                login_page.locators["login_button"]
            )
        )
        print("✔️ 로그인 페이지 이탈 확인")

        wait.until(
        EC.element_to_be_clickable(gnd_component.locators["person_icon"])
        ) 
        # 8. 언어 변경 유지 확인

        gnd_component.click_person_icon()

        account_mgmt_element = wait.until(
            EC.visibility_of_element_located(gnd_component.locators["account_management"])
        )
        print(f"✅ 재로그인 후 언어 유지 확인 성공!")
        assert (
            account_mgmt_element.is_displayed()
        ), "재로그인 후 언어 설정이 유지되지 않았습니다."

        driver.refresh()
        print("✔️ 페이지를 새로고침했습니다.")
    
    except Exception as e:
        assert False, f"사용자 아이콘 클릭 실패: {e}"
    
    finally:
        # 언어 원상복구
        if driver is not None:  # 드라이버가 생성되었을 때만 실행

            try:
                print("\n== 언어 설정 원상복구 시작 ==")

                wait = WebDriverWait(driver, 10)

                # 사람 아이콘 클릭
                personl_con = wait.until(
                    EC.element_to_be_clickable(gnd_component.locators["person_icon"])
                )
                personl_con.click()

                # 언어 설정 클릭
                language_setting = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//span[text()='Language Settings']")
                    )
                )
                language_setting.click()

                # 한국어 선택
                language_korean = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//p[text()='한국어(대한민국)']")
                    )
                )
                language_korean.click()

                print("✅ 한국어 원상복구 완료!")

            except Exception as e:
                print(f"⚠️ 언어 설정 원상복구 실패: {e}")
