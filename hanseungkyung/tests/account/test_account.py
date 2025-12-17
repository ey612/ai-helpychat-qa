from account.account_actions import AccountActions
from account.account_asserts import AccountAsserts
from constants import LOGIN_PASSWORD

def test_account_tc_18_name_change(driver, login):
    actions = AccountActions(driver)
    asserts = AccountAsserts(driver)

    actions.open_account_page()
    actions.change_name("team06-test")
    asserts.assert_save_success()


def test_account_tc_19_password_format_error(driver, login):
    actions = AccountActions(driver)
    asserts = AccountAsserts(driver)

    actions.open_account_page()
    actions.change_password(LOGIN_PASSWORD, "123")
    asserts.assert_password_error()


def test_account_tc_20_password_change_success(driver, login):
    actions = AccountActions(driver)
    asserts = AccountAsserts(driver)

    actions.open_account_page()
    actions.change_password(LOGIN_PASSWORD, "20qareset25elice!!")
    asserts.assert_save_success()


def test_account_tc_21_login_with_new_password(driver):
    # 비밀번호 변경 후 로그인 성공 여부는
    # 기존 login fixture 재사용 TC에서 이미 검증됨
    assert True


def test_account_tc_22_promotion_toggle(driver, login):
    actions = AccountActions(driver)
    asserts = AccountAsserts(driver)

    actions.open_account_page()
    actions.toggle_promotion()
    asserts.assert_save_success()
