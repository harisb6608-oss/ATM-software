"""
ADMIN MODULE
=============
Bank-staff-only operations: view accounts, block/unblock cards,
replenish ATM cash, create new accounts.
"""

import random

from account_module import Account


class AdminModule:
    """Bank-staff-only operations: view accounts, block/unblock,
    replenish ATM cash, create new accounts."""

    def __init__(self, account_manager, admin_username="admin", admin_password="admin123"):
        self.account_manager = account_manager
        self.admin_username = admin_username
        self.admin_password = admin_password
        self.atm_cash = 500000.0

    def login(self, username, password):
        return username == self.admin_username and password == self.admin_password

    def view_all_accounts(self):
        print("\n--- All Accounts ---")
        for acc in self.account_manager.all_accounts():
            status = "BLOCKED" if acc.is_blocked else "ACTIVE"
            print(f"{acc.account_no} | Card {acc.card_no} | {acc.customer.name:<15} "
                  f"| {acc.acc_type:<8} | Bal: {acc.balance:>10.2f} | {status}")
        print(f"\nATM Cash Reserve: {self.atm_cash:.2f}")

    def create_account(self, customer, card_no, pin, acc_type="Savings",
                        initial_deposit=0.0):
        account_no = f"AC{random.randint(10000, 99999)}"
        account = Account(account_no, card_no, pin, customer, acc_type, initial_deposit)
        self.account_manager.add_account(account)
        print(f"New account created: {account_no} (Card: {card_no})")
        return account

    def replenish_cash(self, amount):
        self.atm_cash += amount
        print(f"ATM cash replenished by {amount:.2f}. New reserve: {self.atm_cash:.2f}")

    def block_card(self, card_no):
        if self.account_manager.block_account(card_no):
            print(f"Card {card_no} has been blocked.")
        else:
            print("Card not found.")

    def unblock_card(self, card_no):
        if self.account_manager.unblock_account(card_no):
            print(f"Card {card_no} has been unblocked.")
        else:
            print("Card not found.")
