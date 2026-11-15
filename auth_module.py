"""
LOGIN / PIN AUTHENTICATION MODULE
==================================
Handles card + PIN authentication with attempt limiting, and PIN changes.
"""


class AuthModule:
    """Handles card + PIN authentication with attempt limiting."""

    MAX_ATTEMPTS = 3

    def __init__(self, account_manager):
        self.account_manager = account_manager

    def authenticate(self, card_no, pin):
        account = self.account_manager.find_by_card(card_no)

        if account is None:
            print("Card not recognized. Please contact your bank.")
            return None

        if account.is_blocked:
            print("This card is BLOCKED. Please contact your bank.")
            return None

        if account.pin == pin:
            account.failed_pin_attempts = 0
            print(f"\nWelcome, {account.customer.name}!")
            return account

        account.failed_pin_attempts += 1
        remaining = self.MAX_ATTEMPTS - account.failed_pin_attempts
        if remaining <= 0:
            account.is_blocked = True
            print("Incorrect PIN. Too many attempts — card has been BLOCKED.")
        else:
            print(f"Incorrect PIN. {remaining} attempt(s) remaining.")
        return None

    def change_pin(self, account, old_pin, new_pin):
        if account.pin != old_pin:
            print("Old PIN is incorrect.")
            return False
        if not (new_pin.isdigit() and len(new_pin) == 4):
            print("New PIN must be exactly 4 digits.")
            return False
        account.pin = new_pin
        print("PIN changed successfully.")
        return True
