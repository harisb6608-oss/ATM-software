"""
CUSTOMER MODULE
===============
Holds personal details of a bank customer.
"""


class Customer:
    """Holds personal details of a bank customer."""

    def __init__(self, customer_id, name, phone, email):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone
        self.email = email

    def __str__(self):
        return f"{self.name} (ID: {self.customer_id}, Phone: {self.phone})"
