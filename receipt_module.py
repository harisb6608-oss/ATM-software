"""
RECEIPT / STATEMENT MODULE
============================
Prints receipts for single transactions and mini/full statements.
"""


class ReceiptModule:
    """Prints receipts for single transactions and mini/full statements."""

    @staticmethod
    def print_receipt(account, transaction):
        print("\n" + "=" * 40)
        print("           ATM TRANSACTION RECEIPT")
        print("=" * 40)
        print(f"Account No : {account.account_no}")
        print(f"Card No    : {account.card_no}")
        print(f"Type       : {transaction.tx_type}")
        print(f"Amount     : {transaction.amount:.2f}")
        print(f"Balance    : {transaction.balance_after:.2f}")
        print(f"Date/Time  : {transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 40)
        print("      Thank you for banking with us!")
        print("=" * 40 + "\n")

    @staticmethod
    def mini_statement(account, count=5):
        print(f"\n--- Mini Statement (last {count}) for {account.account_no} ---")
        recent = account.transactions[-count:]
        if not recent:
            print("No transactions yet.")
        for tx in reversed(recent):
            print(tx)
        print("-" * 55)

    @staticmethod
    def full_statement(account):
        print(f"\n--- Full Statement for {account.account_no} ---")
        if not account.transactions:
            print("No transactions yet.")
        for tx in account.transactions:
            print(tx)
        print("-" * 55)
