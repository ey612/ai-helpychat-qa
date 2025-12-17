from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def login_with_invalid_id(driver, wait, invalid_id: str, password: str):
    id_input = wait.until(
        EC.presence_of_element_located((By.NAME, "loginId"))
    )
    id_input.clear()
    id_input.send_keys(invalid_id)

    pw_input = wait.until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    pw_input.clear()
    pw_input.send_keys(password)

    login_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    login_button.click()