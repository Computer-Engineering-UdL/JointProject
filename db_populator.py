import random
from datetime import timedelta
from django.utils import timezone
from faker import Faker
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "JointProject.settings")
django.setup()

from Reception.models import HotelUser, Client, Worker, Room, RoomReservation, CheckIn, Despeses, ExtraCosts
from Cleaner.models import Cleaning_Material, Stock, CleanedRoom
from Reception.config import Config as c

fake = Faker()


def create_users(n) -> None:
    """Populate the User table with n entries."""
    for _ in range(n):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        username = f"{first_name.lower()}_{last_name.lower()}"
        user = HotelUser.objects.create_user(username=username, email=email, password='password')
        user.save()
        print(f'Created User: {username}')


def populate_clients(n) -> None:
    """Populate the Client table with n entries."""
    for _ in range(n):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        username = f"{first_name.lower()}_{last_name.lower()}"
        phone_number = fake.phone_number()
        id_number = fake.ssn()
        is_hosted = random.choice([True, False])

        client = Client.objects.create_user(
            username=username,
            email=email,
            password='password',
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            id_number=id_number,
            is_hosted=is_hosted
        )
        client.save()
        print(f'Created Client: {client.username}')


def populate_rooms(n) -> None:
    """Populate the Room table with n entries, assigning room numbers based on type."""
    room_types = c.get_room_types()[1:]
    print(room_types)
    room_counts = {room_type[0]: c.get_room_number_range(room_type[0])[0] for room_type in room_types}

    for i in range(n):
        room_type_choice = random.choice(room_types)
        room_type = room_type_choice[0]

        start, end = c.get_room_number_range(room_type)
        room_number = room_counts[room_type]
        room_counts[room_type] += 1

        if room_number > end:
            room_number = start
            room_counts[room_type] = start + 1

        room_price = c.get_room_prices_per_type(room_type)
        room = Room(
            room_num=room_number,
            room_type=room_type,
            is_clean=random.choice([True, False]),
            is_taken=random.choice([True, False]),
            room_price=room_price
        )
        room.save()
        print(f'Created Room: {room.room_num} - Type: {room_type} - Price: {room_price}')


def populate_reservations(n) -> None:
    """Populate the RoomReservation table with n entries."""
    pension_types = c.get_pension_types()
    for _ in range(n):
        client = Client.objects.order_by('?').first()
        room = Room.objects.order_by('?').first()
        days_away = random.randint(1, 30)
        duration = random.randint(1, 15)
        entry_date = timezone.now().date() + timedelta(days=days_away)
        exit_date = entry_date + timedelta(days=duration)
        pension_choice = random.choice(pension_types)
        pension_type = pension_choice[0]
        num_guests = random.randint(1, 4)
        reservation = RoomReservation(
            client=client,
            room=room,
            entry=entry_date,
            exit=exit_date,
            num_guests=num_guests,
            pension_type=pension_type,
            is_active=True,
            check_in_active=random.choice([True, False]),
            check_out_active=random.choice([True, False])
        )
        reservation.save()
        print(f'Created Reservation: Room {reservation.room.room_num} from {reservation.entry} to {reservation.exit}'
              f' with pension type {pension_type}')


def print_bar(length=75, new_line=True) -> None:
    """Print a bar of a certain length."""
    if new_line:
        print("─" * length)
    else:
        print("─" * length, end='')


def populate(function, entries: int) -> None:
    """Populate a table in the database with a certain amount of entries."""
    print_bar()
    function_name = function.__name__
    if function_name.startswith('populate_'):
        table_name = function_name[len('populate_'):]
    else:
        table_name = function_name
    table_title = table_name.replace('_', ' ').title()
    print(f"Populating {entries} entries on {table_title} in the database...")
    function(entries)
    print_bar()


def main() -> None:
    """Populate the database with random data."""
    print("Starting to populate the database...")
    populate(create_users, 10)
    populate(populate_clients, 10)
    populate(populate_rooms, 10)
    populate(populate_reservations, 10)
    print("Finished populating the database.")


if __name__ == "__main__":
    main()
