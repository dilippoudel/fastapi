import pytest
from app.calculation import add, BankAccount

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)
# this decorator is to use the parameterize to test with various input.
@pytest.mark.parametrize("x, y, result", [
    (2, 4, 6),
    (5, -3, 2),
    (8, 0, 8)
])
def test_add(x, y, result):
    assert add(x, y) == result

"""Testing Bank account class."""
def test_bank_bank_default_amount(zero_bank_account):
    """Test for initial balance of bank acc."""
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_withdraw(bank_account):
    bank_account.deposit(30)
    bank_account.withdraw(10)
    assert bank_account.balance == 70


def test_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 4) == 55


"""Code example of test case with fixture and parameterize together."""
@pytest.mark.parametrize("deposited, withdrew, result", [
    (200, 40, 160),
    (500, 300, 200),
    (80, 8, 72)
])
def test_bank_transactions(zero_bank_account, deposited, withdrew, result):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == result


def test_insufficient_funds(bank_account):
    with pytest.raises(Exception):
        bank_account.withdraw(200)