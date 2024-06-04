import random

from User.validators import get_nif_word, is_valid_dni


def rand_dni_numbers() -> str:
    """Generate random DNI numbers."""
    return ''.join([str(random.randint(0, 9)) for _ in range(8)])


def add_dni_letter(dni) -> str:
    """Add the letter to the DNI number."""
    return dni + get_nif_word(dni)


def gen_dni() -> str:
    """Generate a random DNI number."""
    dni_numbers = rand_dni_numbers()
    return add_dni_letter(dni_numbers)


def save_dni(dni):
    """Save the DNI number."""
    with open("dni.txt", "a") as file:
        file.write(f"{dni}\n")


def main() -> None:
    for _ in range(50):
        dni = gen_dni()

        if is_valid_dni(dni):
            save_dni(dni)
        else:
            print(f"Invalid DNI: {dni}")


if __name__ == '__main__':
    main()
