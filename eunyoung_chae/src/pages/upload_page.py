from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UploadPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
        # [+] 버튼 클릭 -> [파일 업로드] 버튼 클릭 ( 파일 선택 UI 나오게 하는 것 )
    def open_file_upload_dialog(self):
        plus_icon = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="plusIcon"]')
        plus_icon.click()
        
        upload_file_btn = self.driver.find_element(By.XPATH, "//span[text()='파일 업로드']")
        upload_file_btn.click()

        # 파일 선택 + [열기] 버튼 클릭
    def upload_file(self, file_path):
        file_input = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
        )
        file_input.send_keys(file_path)
    
    
    def upload_multiple_files(self, file_paths: list[str]):
        """
        여러 파일을 동시에 업로드한다.
        Selenium 규칙상 '\\n'으로 경로를 이어서 전달
        """
        files_to_send = '\n'.join(file_paths)

        file_input = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
        )
        file_input.send_keys(files_to_send)