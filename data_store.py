"""
DATA STORE
==========
Seeds demo customers and accounts for testing the ATM system.
"""

from customer_module import Customer
from account_module import Account


class DataStore:
    @staticmethod
    def seed_data(account_manager):
        cust1 = Customer("C001", "Arun Kumar", "9876543210", "arun@example.com")
        cust2 = Customer("C002", "Priya Raman", "9123456780", "priya@example.com")

        acc1 = Account("AC10001", "1001", "1234", cust1, "Savings", balance=15000.0)
        acc2 = Account("AC10002", "1002", "5678", cust2, "Current", balance=42000.0)

        account_manager.add_account(acc1)
        account_manager.add_account(acc2)
