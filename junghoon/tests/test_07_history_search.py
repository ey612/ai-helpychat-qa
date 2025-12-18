import pytest
from junghoon.login import init_driver, login
from junghoon.history_search import (
    open_search_history,
    input_search_text,
    click_history_result,
)
import time

@pytest.mark.history
def test_search_and_click_hello():
    driver, wait = init_driver()

    try:
        login(driver, wait)
        open_search_history(driver, wait)
        
        keyword = "안녕하세요"
        time.sleep(2)
        input_search_text(driver, wait, keyword)
        time.sleep(2)
        click_history_result(driver, wait, keyword)
        time.sleep(2)
        # 실제 검증
        assert keyword in driver.page_source
    finally:
        # driver.quit()
        pass