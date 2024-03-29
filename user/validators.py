import re


def is_valid_dni(dni):
    """Check if the DNI is valid."""
    return re.match(r"\d{8}[A-Za-z]$", dni)


def is_valid_nie(nie):
    """Check if the NIE is valid."""
    return re.match(r"[XYZ]\d{7}[A-Za-z]$", nie)


def is_valid_passport(passport_number):
    """Check if the passport number is valid."""
    return len(passport_number) <= 9


def is_valid_id_number(id_number):
    """Check if the ID number is valid."""
    return is_valid_dni(id_number) or is_valid_nie(id_number) or is_valid_passport(id_number)


def is_valid_phone(phone_number):
    """Check if the phone number is valid."""
    return re.match(r"\d{9}$", phone_number)
