from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import AI_COMPLETE, REGENERATE_BTN

def click_regenerate(driver, index: int = 0):
    """
    index 번째 '다시 생성' 버튼 클릭 (기본: 0 = 첫 번째)
    """
    try:
        buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((
                By.CSS_SELECTOR,
                "button.MuiButtonBase-root.MuiIconButton-root[aria-label='다시 생성']"
            ))
        )

        if index >= len(buttons):
            raise Exception(f"요청한 index={index}, 실제 버튼 개수={len(buttons)}")

        btn = buttons[index]
        btn.click()

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, AI_COMPLETE))
        )
        print(f"🔄 2번째 질문'다시 생성' 버튼 클릭 완료")

    except Exception as e:
        print("⚠ 다시 생성 실패:", e)