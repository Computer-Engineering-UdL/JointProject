import random
from datetime import timedelta
from django.utils import timezone
from faker import Faker
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "JointProject.settings")
django.setup()

from Reception.models import HotelUser, Client, Worker, Room, RoomReservation, CheckIn, Despeses, ExtraCosts
from Cleaner.models import CleaningMaterial, Stock, CleanedRoom
from Restaurant.models import RestaurantReservation
from Reception.config import Config as c
from Restaurant.config import Config as rc
from User.gen_dni import gen_dni

fake = Faker('es_ES')

IMAGE_SRC = "media/cleaning_materials/"


def create_users(n: int) -> None:
    """Populate the User table with n entries."""
    for _ in range(n):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        username = f"{first_name.lower()}_{last_name.lower()}"
        user = HotelUser.objects.create_user(
            username=username,
            email=email,
            password='password',
            first_name=first_name,
            last_name=last_name,
            phone_number=fake.phone_number(),
            id_number=gen_dni()
        )
        user.save()
        print(f'Created User: {username}')


def populate_clients(n: int) -> None:
    """Populate the Client table with n entries."""
    for _ in range(n):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        username = f"{first_name.lower()}_{last_name.lower()}"
        phone_number = fake.phone_number()
        id_number = gen_dni()
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


def populate_rooms(n: int) -> None:
    """Populate the Room table with n entries, assigning room numbers based on type."""
    room_types = c.get_room_types()[1:]
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


def populate_reservations(n: int) -> None:
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
        room_type = room.room_type
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
        print(
            f'Created Reservation: Room {reservation.room.room_num} [{room_type}] from {reservation.entry} '
            f'to {reservation.exit} with pension type {pension_type}')


def create_cleaning_materials(n: int) -> None:
    """Populate the Cleaning_Material table with n entries."""
    for _ in range(n):
        material_name = fake.word()
        image = random.choice([f'{IMAGE_SRC}/{i}' for i in os.listdir(IMAGE_SRC)]).lstrip('media/')
        cleaning_material = CleaningMaterial.objects.create(
            material_name=material_name,
            image=image
        )
        cleaning_material.save()
        print(f'Created Cleaning Material: {cleaning_material.material_name}')


def populate_stock(n: int) -> None:
    """Populate the Stock table with n entries."""
    cleaning_materials = CleaningMaterial.objects.all()
    if not cleaning_materials.exists():
        print("No cleaning materials available to create stock.")
        return

    for _ in range(n):
        material = random.choice(cleaning_materials)
        price = random.uniform(1.0, 100.0).__round__(2)
        is_available = random.choice([True, False])
        stock = Stock.objects.create(
            material=material,
            price=price,
            is_available=is_available,
            is_active=True
        )
        stock.save()
        available_msg = 'Available' if stock.is_available else 'Not Available'
        print(f'Created Stock: {stock.material.material_name} - Price: {stock.price} - {available_msg}')


def populate_cleaned_rooms(n: int) -> None:
    """Populate the CleanedRoom table with n entries."""
    rooms = Room.objects.all()
    if not rooms.exists():
        print("No rooms available to create cleaned room records.")
        return

    for _ in range(n):
        room = random.choice(rooms)
        missing_objects = fake.word() if random.choice([True, False]) else ''
        need_towels = random.randint(0, 5)
        additional_comments = fake.text() if random.choice([True, False]) else ''
        is_cleaned = random.choice([True, False])
        cleaned_room = CleanedRoom.objects.create(
            room=room,
            missing_objects=missing_objects,
            need_towels=need_towels,
            additional_comments=additional_comments,
            is_cleaned=is_cleaned
        )
        cleaned_room.save()
        cleaned_msg = 'Cleaned' if cleaned_room.is_cleaned else 'Not Cleaned'
        print(f'Created Cleaned Room: Room {cleaned_room.room.room_num} - {cleaned_msg}')


def populate_restaurant_reservations(n):
    """Populate the RestaurantReservation table with n entries, ensuring no duplicates for the same day and client."""
    for _ in range(n):
        valid_reservation = False
        while not valid_reservation:
            client = Client.objects.order_by('?').first()
            num_guests = random.randint(1, rc.MAX_GUESTS_PER_RESERVATION)
            entry_date = timezone.now().date() + timedelta(days=random.randint(1, 30))

            if not RestaurantReservation.objects.filter(client=client, day=entry_date).exists():
                reservation = RestaurantReservation(
                    client=client,
                    num_guests=num_guests,
                    day=entry_date,
                    is_active=random.choice([True, False])
                )
                reservation.save()
                print(
                    f'Created Restaurant Reservation: {reservation.client.username} - Guests: {reservation.num_guests}')
                valid_reservation = True
            else:
                print(f'Skipping duplicate reservation for {client.username} on {entry_date}')


def print_bar(length: int = 75, new_line: bool = True) -> None:
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
    populate(create_cleaning_materials, 10)
    populate(populate_stock, 10)
    populate(populate_cleaned_rooms, 10)
    populate(populate_restaurant_reservations, 10)
    print("Finished populating the database.")


if __name__ == "__main__":
    main()
