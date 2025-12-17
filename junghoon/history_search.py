from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def open_search_history(driver, wait: WebDriverWait):
    """
    좌측 메뉴에서 '검색' 메뉴 클릭
    """
    search_menu = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(), '검색')]")
        )
    )
    search_menu.click()


def input_search_text(driver, wait: WebDriverWait, keyword: str):
    """
    히스토리 검색 입력창에 keyword 입력 후 엔터
    """
    search_input = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[placeholder='Search']")
        )
    )
    search_input.clear()
    search_input.send_keys(keyword)
    search_input.send_keys(Keys.ENTER)


def click_history_result(driver, wait, keyword):
    link = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                f"//a[contains(@class,'MuiListItemButton')]"
                f"//span[contains(text(), '{keyword}')]"
            )
        )
    )

    # MUI 안정화용 JS 클릭
    driver.execute_script("arguments[0].click();", link)