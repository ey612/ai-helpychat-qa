# tests/account/test_account.py
import time

import pytest

from constants import LOGIN_PASSWORD
from account.account_actions import AccountActions


# ✅ 네가 지정한 새 비밀번호를 여기 고정
NEW_PASSWORD = "20qareset25elice!!"


@pytest.mark.account
def test_account_tc_18_name_change(driver, login):
    actions = AccountActions(driver)
    actions.open_account_page()

    # ✅ 항상 다른 이름으로(완료 버튼 비활성 방지)
    new_name = f"team06_test_{int(time.time())}"
    actions.change_name(new_name)


@pytest.mark.account
def test_account_tc_19_password_format_error(driver, login):
    actions = AccountActions(driver)
    actions.open_account_page()

    # 예: 짧은 비번(형식 오류 유도)
    actions.change_password(LOGIN_PASSWORD, "123")


@pytest.mark.account
def test_account_tc_20_password_change_success(driver, login):
    actions = AccountActions(driver)
    actions.open_account_page()

    actions.change_password(LOGIN_PASSWORD, NEW_PASSWORD)


@pytest.mark.account
def test_account_tc_21_login_with_new_password(driver, login_with_new_password):
    # fixture에서 검증 완료 처리
    assert True


@pytest.mark.account
def test_account_tc_22_promotion_toggle(driver, login):
    actions = AccountActions(driver)
    actions.open_account_page()

    actions.toggle_promotion_marketing()
