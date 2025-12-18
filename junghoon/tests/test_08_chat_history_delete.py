# junghoon/tests/test_chat_history_delete.py

import pytest
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from junghoon.login import init_driver, login
from junghoon.chat_sendmessage import send_message
from junghoon.chat_history_delete import delete_history


@pytest.fixture(scope="function")
def driver():
    """
    - 브라우저/대기 객체 생성
    - 로그인
    - 히스토리 한 개 생성 (이름 변경 없이)
    - 테스트 종료 후 브라우저 종료
    """
    driver, wait = init_driver()
    login(driver, wait)

    # 히스토리 생성용 메시지 전송
    # 👉 이 텍스트 일부로 히스토리를 찾아서 삭제할 거예요.
    send_message(driver, "히스토리 삭제 테스트용 메시지입니다.")

    yield driver

    driver.quit()


def _get_history_titles(driver):
    """현재 화면에 보이는 히스토리 제목 텍스트 리스트를 반환 (디버깅용)"""
    wait = WebDriverWait(driver, 10)
    histories = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "p.MuiTypography-root")
        )
    )
    return [h.text for h in histories]


def test_delete_history_without_rename(driver):
    """
    이름 변경 없이, 생성된 히스토리를 바로 삭제하는 테스트
    """
    # 👉 히스토리 제목에 포함될 것으로 기대하는 텍스트 일부
    target_keyword = "히스토리 삭제 테스트용 메시지입니다"

    # 삭제 전 상태 로그
    before_titles = _get_history_titles(driver)
    print("📝 삭제 전 히스토리 목록:")
    for t in before_titles:
        print("  -", t)

    # 1) 삭제 실행 (제목 전체가 아니어도, 포함 관계면 삭제 대상 발견 가능)
    delete_history(driver, target_keyword)

    wait = WebDriverWait(driver, 10)

    # 2) 해당 텍스트를 가진 <p> 요소가 DOM에서 사라질 때까지 기다림
    try:
        wait.until_not(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"//p[contains(@class, 'MuiTypography-root') and contains(., '{target_keyword}')]",
                )
            )
        )
    except Exception:
        # 안 사라져도 아래에서 한 번 더 검사
        pass

    # 3) 히스토리 목록 다시 읽기 (stale 방지용 재시도 포함)
    for attempt in range(3):
        try:
            after_titles = _get_history_titles(driver)
            print(f"🧹 삭제 후 히스토리 목록 (시도 {attempt + 1}):")
            for t in after_titles:
                print("  -", t)

            still_exists = any(target_keyword in t for t in after_titles)
            break
        except StaleElementReferenceException:
            if attempt == 2:
                raise

    assert not still_exists, f"'{target_keyword}' 를 포함한 히스토리 항목이 아직 남아 있습니다."