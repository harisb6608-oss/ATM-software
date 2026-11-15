"""
TRANSACTION MODULE
===================
Handles deposits, withdrawals, and transfers between accounts.
Depends on the Balance Update Module for safe credit/debit operations.
"""

import datetime


class Transaction:
    def __init__(self, tx_id, tx_type, amount, balance_after, details=""):
        self.tx_id = tx_id
        self.tx_type = tx_type
        self.amount = amount
        self.balance_after = balance_after
        self.timestamp = datetime.datetime.now()
        self.details = details

    def __str__(self):
        ts = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        sign = "+" if self.tx_type in ("Deposit", "Transfer In") else "-"
        return (f"[{ts}] {self.tx_type:<14} {sign}{self.amount:>10.2f}  "
                f"Bal: {self.balance_after:>10.2f}  {self.details}")


class TransactionModule:
    """Handles deposits, withdrawals, and transfers between accounts."""

    def __init__(self, account_manager, balance_module):
        self.account_manager = account_manager
        self.balance_module = balance_module
        self._tx_counter = 100000

    def _next_tx_id(self):
        self._tx_counter += 1
        return f"TXN{self._tx_counter}"

    def deposit(self, account, amount):
        if amount <= 0:
            print("Deposit amount must be positive.")
            return False
        self.balance_module.credit(account, amount)
        tx = Transaction(self._next_tx_id(), "Deposit", amount, account.balance)
        account.transactions.append(tx)
        print(f"Deposited {amount:.2f}. New balance: {account.balance:.2f}")
        return True

    def withdraw(self, account, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return False
        if amount % 100 != 0:
            print("Please enter an amount in multiples of 100.")
            return False
        if account.withdrawn_today + amount > account.daily_limit:
            print(f"Daily withdrawal limit ({account.daily_limit:.2f}) exceeded.")
            return False
        try:
            self.balance_module.debit(account, amount)
        except ValueError as e:
            print(str(e))
            return False
        account.withdrawn_today += amount
        tx = Transaction(self._next_tx_id(), "Withdrawal", amount, account.balance)
        account.transactions.append(tx)
        print(f"Please collect your cash: {amount:.2f}")
        print(f"New balance: {account.balance:.2f}")
        return True

    def transfer(self, from_account, to_card_no, amount):
        if amount <= 0:
            print("Transfer amount must be positive.")
            return False
        to_account = self.account_manager.find_by_card(to_card_no)
        if to_account is None:
            print("Destination account not found.")
            return False
        if to_account.card_no == from_account.card_no:
            print("Cannot transfer to the same account.")
            return False
        try:
            self.balance_module.debit(from_account, amount)
        except ValueError as e:
            print(str(e))
            return False
        self.balance_module.credit(to_account, amount)

        tx_out = Transaction(self._next_tx_id(), "Transfer Out", amount,
                              from_account.balance, details=f"To {to_card_no}")
        tx_in = Transaction(self._next_tx_id(), "Transfer In", amount,
                             to_account.balance, details=f"From {from_account.card_no}")
        from_account.transactions.append(tx_out)
        to_account.transactions.append(tx_in)

        print(f"Transferred {amount:.2f} to card {to_card_no}.")
        print(f"New balance: {from_account.balance:.2f}")
        return True
