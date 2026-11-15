"""
ACCOUNT MANAGEMENT MODULE
=========================
Represents bank accounts linked to customers and ATM cards, and manages
the overall collection of accounts (create, find, block, unblock).
"""


class Account:
    """Represents a bank account linked to a customer and ATM card."""

    def __init__(self, account_no, card_no, pin, customer, acc_type="Savings",
                 balance=0.0, daily_limit=25000.0):
        self.account_no = account_no
        self.card_no = card_no
        self.pin = pin
        self.customer = customer
        self.acc_type = acc_type
        self.balance = balance
        self.daily_limit = daily_limit
        self.withdrawn_today = 0.0
        self.is_blocked = False
        self.failed_pin_attempts = 0
        self.transactions = []  # list of Transaction objects

    def reset_daily_limit(self):
        self.withdrawn_today = 0.0


class AccountManager:
    """Manages the collection of accounts (create, find, block, unblock)."""

    def __init__(self):
        self.accounts = {}  # card_no -> Account

    def add_account(self, account):
        self.accounts[account.card_no] = account

    def find_by_card(self, card_no):
        return self.accounts.get(card_no)

    def block_account(self, card_no):
        acc = self.find_by_card(card_no)
        if acc:
            acc.is_blocked = True
            return True
        return False

    def unblock_account(self, card_no):
        acc = self.find_by_card(card_no)
        if acc:
            acc.is_blocked = False
            acc.failed_pin_attempts = 0
            return True
        return False

    def all_accounts(self):
        return list(self.accounts.values())
