from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class ChatPage:
    def __init__(self, driver):
        self.wait = WebDriverWait(driver, 10)
        self.driver = driver

    def input_message(self, value: str = ""):
        chat_input = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='input']"))
        )
        chat_input.send_keys(value)
        return chat_input

    def click_send_button(self):
        send_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Send']"))
        )
        send_button.click()
        return send_button

    def send_message(self, value: str = ""):
        self.input_message(value)
        self.click_send_button()
        return self.driver

    def check_ai_response(self):
        ai_response = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[data-status='complete']")
            )
        )
        return ai_response

    def click_regenerate_button(self):
        regenerate_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[aria-label='다시 생성']")
            )
        )
        regenerate_button.click()
        return regenerate_button

    def click_prev_answer_button(self):
        prev_answer_button = self.wait.until(
            EC.element_to_be_clickable(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'button:has(svg[data-testid="chevron-leftIcon"])')
                )
            )
        )
        prev_answer_button.click()
