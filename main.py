"""
ATM SOFTWARE SYSTEM - MAIN CONTROLLER
=======================================
Ties together all seven modules into a menu-driven console ATM:

    1. Login / PIN Authentication Module -> auth_module.py
    2. Customer Module                   -> customer_module.py
    3. Account Management Module         -> account_module.py
    4. Transaction Module                -> transaction_module.py
    5. Balance Update Module             -> balance_module.py
    6. Receipt / Statement Module        -> receipt_module.py
    7. Admin Module                      -> admin_module.py

Run with:
    python main.py

Default test data (see data_store.py):
    Card No: 1001   PIN: 1234   (Savings)
    Card No: 1002   PIN: 5678   (Current)
    Admin Username: admin       Admin Password: admin123
"""

import random
import sys

from account_module import AccountManager
from auth_module import AuthModule
from balance_module import BalanceModule
from transaction_module import TransactionModule
from receipt_module import ReceiptModule
from admin_module import AdminModule
from data_store import DataStore
from customer_module import Customer


class ATM:
    def __init__(self):
        self.account_manager = AccountManager()
        DataStore.seed_data(self.account_manager)

        self.auth_module = AuthModule(self.account_manager)
        self.balance_module = BalanceModule()
        self.transaction_module = TransactionModule(self.account_manager, self.balance_module)
        self.receipt_module = ReceiptModule()
        self.admin_module = AdminModule(self.account_manager)

    def run(self):
        print("=" * 45)
        print("        WELCOME TO PYTHON BANK ATM")
        print("=" * 45)
        while True:
            print("\n1. Customer Login")
            print("2. Admin Login")
            print("3. Exit")
            choice = input("Select an option: ").strip()

            if choice == "1":
                self.customer_flow()
            elif choice == "2":
                self.admin_flow()
            elif choice == "3":
                print("Thank you for using Python Bank ATM. Goodbye!")
                sys.exit(0)
            else:
                print("Invalid option, try again.")

    # -----------------------------------------------------------------
    def customer_flow(self):
        card_no = input("Enter Card Number: ").strip()
        pin = input("Enter 4-digit PIN: ").strip()
        account = self.auth_module.authenticate(card_no, pin)
        if account is None:
            return
        self.customer_menu(account)

    def customer_menu(self, account):
        while True:
            print("\n----- ATM MENU -----")
            print("1. Balance Inquiry")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Transfer Funds")
            print("5. Mini Statement")
            print("6. Full Statement")
            print("7. Change PIN")
            print("8. Logout")
            choice = input("Select an option: ").strip()

            if choice == "1":
                print(f"Current Balance: {self.balance_module.get_balance(account):.2f}")

            elif choice == "2":
                amount = self._read_amount("Enter deposit amount: ")
                if amount is not None and self.transaction_module.deposit(account, amount):
                    self.receipt_module.print_receipt(account, account.transactions[-1])

            elif choice == "3":
                amount = self._read_amount("Enter withdrawal amount: ")
                if amount is not None and self.transaction_module.withdraw(account, amount):
                    self.receipt_module.print_receipt(account, account.transactions[-1])

            elif choice == "4":
                to_card = input("Enter destination card number: ").strip()
                amount = self._read_amount("Enter transfer amount: ")
                if amount is not None:
                    self.transaction_module.transfer(account, to_card, amount)

            elif choice == "5":
                self.receipt_module.mini_statement(account)

            elif choice == "6":
                self.receipt_module.full_statement(account)

            elif choice == "7":
                old_pin = input("Enter current PIN: ").strip()
                new_pin = input("Enter new 4-digit PIN: ").strip()
                self.auth_module.change_pin(account, old_pin, new_pin)

            elif choice == "8":
                print("Logging out... Thank you!")
                break
            else:
                print("Invalid option, try again.")

    @staticmethod
    def _read_amount(prompt):
        raw = input(prompt).strip()
        try:
            amount = float(raw)
            return amount
        except ValueError:
            print("Please enter a valid number.")
            return None

    # -----------------------------------------------------------------
    def admin_flow(self):
        username = input("Admin username: ").strip()
        password = input("Admin password: ").strip()
        if not self.admin_module.login(username, password):
            print("Invalid admin credentials.")
            return
        print("Admin login successful.")
        self.admin_menu()

    def admin_menu(self):
        while True:
            print("\n----- ADMIN MENU -----")
            print("1. View All Accounts")
            print("2. Create New Account")
            print("3. Block Card")
            print("4. Unblock Card")
            print("5. Replenish ATM Cash")
            print("6. Logout")
            choice = input("Select an option: ").strip()

            if choice == "1":
                self.admin_module.view_all_accounts()

            elif choice == "2":
                name = input("Customer name: ").strip()
                phone = input("Phone: ").strip()
                email = input("Email: ").strip()
                card_no = input("New card number: ").strip()
                pin = input("Set 4-digit PIN: ").strip()
                acc_type = input("Account type (Savings/Current): ").strip() or "Savings"
                deposit = self._read_amount("Initial deposit: ") or 0.0
                customer_id = f"C{random.randint(100, 999)}"
                customer = Customer(customer_id, name, phone, email)
                self.admin_module.create_account(customer, card_no, pin, acc_type, deposit)

            elif choice == "3":
                card_no = input("Card number to block: ").strip()
                self.admin_module.block_card(card_no)

            elif choice == "4":
                card_no = input("Card number to unblock: ").strip()
                self.admin_module.unblock_card(card_no)

            elif choice == "5":
                amount = self._read_amount("Amount to add to ATM cash: ")
                if amount is not None:
                    self.admin_module.replenish_cash(amount)

            elif choice == "6":
                print("Admin logged out.")
                break
            else:
                print("Invalid option, try again.")


if __name__ == "__main__":
    atm = ATM()
    atm.run()
