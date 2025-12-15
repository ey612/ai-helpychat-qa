import pytest
from selenium import webdriver

@pytest.fixture
def driver():
    d = webdriver.Chrome()
    d.implicitly_wait(3)
    yield d
    d.quit()
