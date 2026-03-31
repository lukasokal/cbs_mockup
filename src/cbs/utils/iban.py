"""IBAN generation helper (simplified for mockup)."""

import random
import string


def generate_iban(country: str = "SK") -> str:
    """Generate a pseudo-random IBAN for the given country code.

    This is a simplified generator for demonstration purposes only.
    Real IBAN generation requires proper check-digit calculation (ISO 7064).
    """
    bank_code = "1200"
    account_number = "".join(random.choices(string.digits, k=16))
    # Simplified check digits (real implementation would use mod-97)
    check_digits = str(random.randint(10, 99))
    return f"{country.upper()}{check_digits}{bank_code}{account_number}"


def mask_card_number(length: int = 16) -> str:
    """Generate a masked card number like 4*** **** **** 1234."""
    first = str(random.choice([4, 5]))  # 4=Visa, 5=MC
    last_four = "".join(random.choices(string.digits, k=4))
    return f"{first}{'*' * (length - 5)}{last_four}"


def generate_reference(prefix: str = "PAY") -> str:
    """Generate a unique-ish transaction reference."""
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
    return f"{prefix}-{suffix}"
