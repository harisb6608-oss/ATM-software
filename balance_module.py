"""
BALANCE UPDATE MODULE
======================
Responsible purely for reading/updating account balances safely.
"""


class BalanceModule:
    """Responsible purely for reading/updating account balances safely."""

    @staticmethod
    def get_balance(account):
        return account.balance

    @staticmethod
    def credit(account, amount):
        account.balance += amount

    @staticmethod
    def debit(account, amount):
        if amount > account.balance:
            raise ValueError("Insufficient funds.")
        account.balance -= amount
