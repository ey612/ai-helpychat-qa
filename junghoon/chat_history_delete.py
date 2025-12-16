from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

def delete_history(driver, history_text: str, wait_time: int = 10):
    wait = WebDriverWait(driver, wait_time)

    # 1) 히스토리 텍스트 찾기
    histories = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "p.MuiTypography-root")
        )
    )

    target = None
    for h in histories:
        if history_text in h.text:
            target = h
            break

    if not target:
        print(f"⚠ 삭제 대상 히스토리 '{history_text}' 를 찾지 못했습니다.")
        return

    # 2) 스크롤 + 호버
    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});", target
    )
    ActionChains(driver).move_to_element(target).perform()
    time.sleep(0.5)

    # 3) 점 3개 메뉴 클릭
    menu_btn = target.find_element(
        By.XPATH, ".//following::button[1]"
    )
    driver.execute_script("arguments[0].click();", menu_btn)
    
    # 4) 메뉴에서 '삭제' 클릭
    delete_menu = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//*[text()='삭제']")
        )
    )
    delete_menu.click()
    print("🗑️ 메뉴에서 '삭제' 클릭 완료")

    # 5) 팝업 '삭제' 버튼 클릭
    confirm_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space(text())='삭제']")
        )
    )
    confirm_btn.click()
    print("✅ 팝업 '삭제' 버튼 클릭 완료")