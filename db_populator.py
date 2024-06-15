import os
import random
from datetime import timedelta

import django
from django.utils import timezone
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "JointProject.settings")
django.setup()

from Reception.models import HotelUser, Client, Worker, Room, RoomReservation, create_despesa, ExtraCosts
from Cleaner.models import CleaningMaterial, Stock, CleanedRoom
from Cleaner.config import MATERIALS_NAMES
from Restaurant.models import RestaurantReservation
from Reception.config import Config as c
from Restaurant.config import Config as rc
from Restaurant.models import ExternalRestaurantClient
from Restaurant.forms import get_available_clients
from User.gen_dni import gen_dni
from User.config import Config as uc

fake = Faker('es_ES')

IMAGE_SRC = "media/cleaning_materials/"


def create_users(n: int) -> None:
    """Populate the User table with n entries."""
    for _ in range(n):
        first_name = fake.first_name()
        last_name = fake.last_name() + random.choice(['', ' ' + fake.last_name()])
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


def create_workers(n: int) -> None:
    """Populate the Worker table with n entries."""
    for _ in range(n):
        first_name = fake.first_name()
        last_name = fake.last_name() + random.choice(['', ' ' + fake.last_name()])
        email = fake.email()
        username = f"{first_name.lower()}_{last_name.lower()}"
        worker_type = random.choice(list(uc.get_worker_type_to_url().keys()))

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

        worker = Worker(hoteluser_ptr_id=user.pk, type=worker_type)
        worker.save_base(raw=True)
        print(f'Created Worker: {username} - Type: {worker_type}')


def populate_clients(n: int) -> None:
    """Populate the Client table with n entries."""
    for _ in range(n):
        first_name = fake.first_name()
        last_name = fake.last_name() + random.choice(['', ' ' + fake.last_name()])
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
    """Populate the Room table with n entries, assigning unique room numbers based on type."""
    room_types = c.get_room_types()[1:]
    room_counts = {room_type[0]: c.get_room_number_range(room_type[0])[0] for room_type in room_types}
    used_room_numbers = set(Room.objects.values_list('room_num', flat=True))

    for _ in range(n):
        room_created = False
        while not room_created:
            room_type_choice = random.choice(room_types)
            room_type = room_type_choice[0]

            start, end = c.get_room_number_range(room_type)
            room_number = room_counts[room_type]

            if start <= room_number <= end and room_number not in used_room_numbers:
                room_price = c.get_room_prices_per_type(room_type)
                room = Room(
                    room_num=room_number,
                    room_type=room_type,
                    is_clean=random.choice([True, False]),
                    is_taken=random.choice([True, False]),
                    room_price=room_price
                )
                room.save()
                used_room_numbers.add(room_number)
                room_counts[room_type] += 1
                room_created = True
                print(f'Created Room: {room.room_num} - Type: {room_type} - Price: {room_price}')
            else:
                room_counts[room_type] += 1
                if room_counts[room_type] > end:
                    room_counts[room_type] = start


def populate_reservations(n: int) -> None:
    """Populate the RoomReservation table with n entries, ensuring no conflicts with existing reservations."""
    pension_types = c.get_pension_types()
    all_rooms = list(Room.objects.all())
    clients = list(Client.objects.all())
    max_attempts = 5

    guest_limits = {
        'No seleccionat': (1, 1),
        'Individual': (1, 1),
        'Double': (1, 2),
        'Suite': (1, 4),
        'Deluxe': (1, 4)
    }

    for _ in range(n):
        reservation_created = False
        attempt = 0

        while not reservation_created and attempt < max_attempts:
            room = random.choice(all_rooms)
            client = random.choice(clients)
            days_away = random.randint(1, 30)
            duration = random.randint(1, 15)
            entry_date = timezone.now().date() + timedelta(days=days_away)
            exit_date = entry_date + timedelta(days=duration)

            if not RoomReservation.objects.filter(room=room, exit__gte=entry_date, entry__lte=exit_date).exists():
                is_active = random.choice([True, False])

                check_in_active = random.choice([True, False])
                check_out_active = check_in_active and random.choice([True, False])

                pension_type = random.choice(pension_types)[0]

                min_guests, max_guests = guest_limits.get(room.room_type, (1, 1))
                num_guests = random.randint(min_guests, max_guests)

                reservation = RoomReservation(
                    client=client,
                    room=room,
                    entry=entry_date,
                    exit=exit_date,
                    num_guests=num_guests,
                    pension_type=pension_type,
                    is_active=is_active,
                    check_in_active=check_in_active,
                    check_out_active=check_out_active
                )
                reservation.save()
                create_despesa(reservation, pension_type, room.room_type)
                print(f'Created Reservation: Room {room.room_num} [{room.room_type}]'
                      f' from {entry_date} to {exit_date} with pension type {pension_type}'
                      f', is active: {is_active}, check-in: {check_in_active}, check-out: {check_out_active}')
                reservation_created = True
            else:
                attempt += 1

        if not reservation_created:
            print("No s'ha pogut crear una reserva per falta d'habitacions disponibles sense conflictes.")


def create_cleaning_materials(n: int) -> None:
    """Populate the Cleaning_Material table with n entries."""
    for i in range(n):
        material_name = list(MATERIALS_NAMES)[i]
        if CleaningMaterial.objects.filter(material_name=material_name).exists():
            print(f'Cleaning Material already exists: {material_name}')
            continue
        image = IMAGE_SRC + MATERIALS_NAMES[material_name]
        image_cleaned = image.lstrip('media/')
        cleaning_material = CleaningMaterial(
            material_name=material_name,
            image=image_cleaned
        )
        cleaning_material.save()
        print(f'Created Cleaning Material: {cleaning_material.material_name}')


def populate_stock(n: int) -> None:
    """Populate the Stock table with n entries."""
    cleaning_materials = CleaningMaterial.objects.all()
    if not cleaning_materials.exists():
        print("No cleaning materials available to create stock.")
        return

    for i in range(n):
        material_name = list(MATERIALS_NAMES)[i]
        material = cleaning_materials.filter(material_name=material_name).first()
        if not material:
            material = CleaningMaterial.objects.create(material_name=material_name)
            material.save()
            print(f'Created Cleaning Material: {material.material_name}')

        if Stock.objects.filter(material=material).exists():
            print(f'Stock already exists for material: {material.material_name}')
            continue
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


def populate_external_clients(n: int) -> None:
    """Populate the ExternalRestaurantClient table with n entries."""
    for _ in range(n):
        first_name = fake.first_name()
        last_name = fake.last_name() + random.choice(['', ' ' + fake.last_name()])
        email = fake.email()
        phone_number = fake.phone_number()

        external_client = ExternalRestaurantClient.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number
        )
        external_client.save()
        print(f'Created External Client: {external_client.first_name} {external_client.last_name}'
              f' - Email: {external_client.email}')


def populate_restaurant_reservations(n: int) -> None:
    """Populate the RestaurantReservation table with n entries, ensuring no duplicates for the same day and client."""
    for _ in range(n):
        is_internal = random.choice([True, False])
        num_guests = random.randint(1, rc.MAX_GUESTS_PER_RESERVATION)
        entry_date = timezone.now().date() + timedelta(days=random.randint(1, 30))

        if is_internal:
            available_clients = get_available_clients()
            if not available_clients.exists():
                print("No available internal clients for reservation on", entry_date)
                continue
            client = available_clients.order_by('?').first()
            reservation_filter = RestaurantReservation.objects.filter(client=client, day=entry_date)
        else:
            client = ExternalRestaurantClient.objects.order_by('?').first()
            reservation_filter = RestaurantReservation.objects.filter(external_client=client, day=entry_date)

        if not reservation_filter.exists():
            reservation = RestaurantReservation(
                client=client if is_internal else None,
                external_client=None if is_internal else client,
                num_guests=num_guests,
                day=entry_date,
                service=random.choice(rc.get_restaurant_services())[0],
                is_active=random.choice([True, False])
            )
            reservation.save()
            client_type = "internal" if is_internal else "external"
            print(f'Created Restaurant Reservation for {client_type}'
                  f' client: {client.username if is_internal else client.first_name}'
                  f' - Guests: {reservation.num_guests}')
        else:
            client_type = "internal" if is_internal else "external"
            print(f'Skipping duplicate reservation for {client_type} client on {entry_date}')


def get_active_reservations_without_expenses():
    """Return all active room reservations without an expense record."""
    return RoomReservation.objects.filter(
        is_active=True,
        despeses__isnull=True
    )


def create_expenses_for_active_reservations() -> None:
    """Create an expense record for each active room reservation without an expense record."""
    active_reservations_without_expenses = get_active_reservations_without_expenses()

    for reservation in active_reservations_without_expenses:
        pension_type = reservation.pension_type
        room_type = reservation.room.room_type

        pension_cost = c.get_pension_cost_per_type(pension_type)
        room_cost = c.get_room_prices_per_type(room_type)

        create_despesa(reservation, pension_type, room_type)

        print(f"Created expense for reservation {reservation.id}: "
              f"Pension cost {pension_cost}, Room type cost {room_cost}")

    print(f"Total expenses created: {active_reservations_without_expenses.count()}")


def create_extra_costs(n: int) -> None:
    """Populate the ExtraCosts table with n entries ensuring no duplicate extra costs type for the same reservation."""
    reservations = RoomReservation.objects.filter(is_active=True, check_in_active=True)
    if not reservations.exists():
        print("No reservations available to create extra costs where check-in is completed.")
        return

    extra_costs_types = c.get_room_extra_costs()

    for _ in range(n):
        reservation = random.choice(list(reservations))
        available_types = list(extra_costs_types)

        used_types = ExtraCosts.objects.filter(room_reservation=reservation).values_list('extra_costs_type', flat=True)
        available_types = [t for t in available_types if t[0] not in used_types]

        if not available_types:
            print(f'No more unique extra costs types available for reservation ID {reservation.id}')
            continue

        extra_costs_type = random.choice(available_types)[0]
        extra_costs_price = round(random.uniform(1.0, 100.0), 2)

        extra_costs = ExtraCosts.objects.create(
            room_reservation=reservation,
            extra_costs_type=extra_costs_type,
            extra_costs_price=extra_costs_price
        )
        print(f'Created Extra Costs: {extra_costs.extra_costs_type} - '
              f'Price: {extra_costs.extra_costs_price} for Reservation ID {reservation.id}')


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


populate_functions = {
    'users': create_users,
    'workers': create_workers,
    'clients': populate_clients,
    'rooms': populate_rooms,
    'reservations': populate_reservations,
    'materials': create_cleaning_materials,
    'stock': populate_stock,
    'cleaned_rooms': populate_cleaned_rooms,
    'external_clients': populate_external_clients,
    'restaurant_reservations': populate_restaurant_reservations,
    'expenses': create_expenses_for_active_reservations,
    'extra_costs': create_extra_costs
}


def main() -> None:
    """Populate the database with random data."""
    print("Starting to populate the database...")
    populate(create_users, 10)
    populate(create_workers, 10)
    populate(populate_clients, 10)
    populate(populate_rooms, 10)
    populate(populate_reservations, 10)
    populate(create_cleaning_materials, len(MATERIALS_NAMES))
    populate(populate_stock, len(MATERIALS_NAMES))
    populate(populate_cleaned_rooms, 10)
    populate(populate_external_clients, 10)
    populate(populate_restaurant_reservations, 20)
    create_expenses_for_active_reservations()
    print("Finished populating the database.")


if __name__ == "__main__":
    main()
