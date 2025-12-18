# -*- coding: utf-8 -*-
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


EMAIL = os.getenv("ELICE_QA_EMAIL", "qa3team0601@elicer.com")
PASSWORD = os.getenv("ELICE_QA_PW", "team06cheerup!")
ACCOUNTS_BASE = os.getenv("ELICE_ACCOUNTS_BASE", "https://accounts.elice.io")
CONTINUE_TO = os.getenv("ELICE_CONTINUE_TO", "")  # 있으면 더 안정
NEW_NAME = os.getenv("ELICE_NEW_NAME", "team06_test")
WEAK_PW = os.getenv("ELICE_WEAK_PW", "1234")
STRONG_PW = os.getenv("ELICE_STRONG_PW", "Team06!!123")


def step(n: int, msg: str):
    print(f"{n}. {msg}")

def ok(msg: str):
    print(f"✅ {msg}")

def info(msg: str):
    print(f"• {msg}")


def build_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    d = webdriver.Chrome(options=options)
    d.set_page_load_timeout(30)
    return d


def wait_click(driver, locators, timeout=12, scope=None, desc="element"):
    last = None
    for by, val in locators:
        try:
            if scope is None:
                el = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, val)))
            else:
                def _f(_):
                    x = scope.find_element(by, val)
                    return x if x.is_displayed() and x.is_enabled() else False
                el = WebDriverWait(driver, timeout).until(_f)
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            el.click()
            return el
        except Exception as e:
            last = e
    raise AssertionError(f"[FAIL] 클릭 실패: {desc}\n마지막 에러: {last}")


def wait_type(driver, locators, text, timeout=12, scope=None, clear=True, desc="input"):
    last = None
    for by, val in locators:
        try:
            if scope is None:
                el = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, val)))
            else:
                def _f(_):
                    x = scope.find_element(by, val)
                    return x if x.is_displayed() else False
                el = WebDriverWait(driver, timeout).until(_f)
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            el.click()
            if clear:
                el.send_keys(Keys.CONTROL, "a")
                el.send_keys(Keys.BACKSPACE)
            el.send_keys(text)
            return el
        except Exception as e:
            last = e
    raise AssertionError(f"[FAIL] 입력 실패: {desc}\n마지막 에러: {last}")


def wait_text_any(driver, keywords, timeout=12):
    def _cond(_):
        src = driver.page_source
        return any(k in src for k in keywords)
    WebDriverWait(driver, timeout).until(_cond)


def find_container_by_label(driver, label_keywords, timeout=12):
    # 라벨 포함 요소 -> 가장 가까운 div/section/li로 범위 제한
    xp = " | ".join([f"//*[contains(normalize-space(.),'{k}')]" for k in label_keywords])
    container_xp = f"({xp})[1]/ancestor::*[self::div or self::section or self::li][1]"
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, container_xp)))


def open_login(driver):
    url = f"{ACCOUNTS_BASE}/accounts/signin"
    if CONTINUE_TO:
        url = f"{ACCOUNTS_BASE}/accounts/signin?continue_to={CONTINUE_TO}"
    driver.get(url)


def do_login(driver, email,_
