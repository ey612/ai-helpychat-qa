import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.pages.login_page import LoginPage
from src.pages.main_page import GnbComponent, LanguageSetting
from src.config.config import EMAIL, PW


# [LANG_TC_001] 프로필 메뉴에서 언어 설정 클릭 시 지원 언어 목록이 표시되는지 확인
def test_001_language_menu_shows_supported_languages(driver):
    wait = WebDriverWait(driver, 10)
    
    # 1. 로그인
    login_page = LoginPage(driver)
    login_page.login(PW, EMAIL)

    # 테스트 로직 실행

    # 1. 언어 설정 메뉴 열기
    gnb = GnbComponent(driver)
    gnb.click_person_icon()
    gnb.click_language_setting()

    # 2. 지원 언어 표시 되는지 확인
    language_setting = LanguageSetting(driver)
    test_passed = language_setting.verify_all_languages_displayed()
    
    # 3. 검증
    assert test_passed, "모든 언어 항목이 드롭다운에 표시되지 않았습니다."

# [LANG_TC_002] 언어 변경 후 재로그인 시 선택한 언어 설정이 유지되는지 확인
def test_002_language_setting_persists_after_relogin(driver):
    wait = WebDriverWait(driver, 10)
    
    try:
        # 1. 로그인
        login_page = LoginPage(driver)
        login_page.login(PW, EMAIL)
    except Exception as e:
        assert False, f"로그인 실패: {e}"

    # 2. 사용자 아이콘 -> 언어 설정 클릭
    gnd_component = GnbComponent(driver)

    try:
        gnd_component.click_person_icon()
        gnd_component.click_language_setting()
        
        # 3. 언어 설정 변경 ( 한국어 -> 영어 )
        language_setting = LanguageSetting(driver)
        language_setting.select_language("American English")

        # 4. 언어 변경 확인 (검증)
        is_displayed = gnd_component.is_account_management_displayed()
        assert is_displayed, "Account Management가 표시되지 않았습니다."

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
