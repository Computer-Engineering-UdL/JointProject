import re


def get_nif_word(dni):
    """Get the NIF letter."""
    words = {0: 'T', 1: 'R', 2: 'W', 3: 'A', 4: 'G', 5: 'M', 6: 'Y', 7: 'F', 8: 'P', 9: 'D', 10: 'X', 11: 'B',
             12: 'N', 13: 'J', 14: 'Z', 15: 'S', 16: 'Q', 17: 'V', 18: 'H', 19: 'L', 20: 'C', 21: 'K', 22: 'E'}

    rest = int(dni) % 23

    return words[rest]


def is_valid_dni(dni):
    """Check if the DNI is valid."""
    if len(dni) != 9 or not dni[:-1].isdigit() or not dni[-1].isalpha():
        return False

    numero_dni = dni[:-1]
    letra_correcta = get_nif_word(numero_dni)
    letra_dada = dni[-1].upper()

    return letra_correcta == letra_dada


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
