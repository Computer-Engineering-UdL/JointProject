class Config:
    @staticmethod
    def get_room_extra_costs():
        return ROOM_EXTRA_COSTS

    @staticmethod
    def get_pension_types():
        return PENSION_TYPE

    @staticmethod
    def get_room_types():
        return ROOM_TYPES

    @staticmethod
    def get_check_in_path(n: int):
        return CHECK_IN_PATH[n]

    @staticmethod
    def get_reservation_path(n: int):
        return RESERVATION_PATH[n]

    @staticmethod
    def get_manage_reservation_path(n: int):
        return MANAGE_RESERVATION[n]

    @staticmethod
    def get_check_out_path(n: int):
        return CHECK_OUT_PATH[n]

    @staticmethod
    def get_admin_tests_path(n: int):
        return ADMIN_TESTS_PATH[n]


ROOM_EXTRA_COSTS = [
    ('Minibar', 'Minibar'),
    ('Desperfectes', 'Desperfectes'),
    ('Servei habitacions', 'Servei habitacions'),
    ('Parking', 'Parking'),
    ('Perdua de claus', 'Perdua de claus'),
]

PENSION_TYPE = [
    ('Sense pensió', 'Sense pensió'),
    ('Esmorzar Buffet', 'Esmorzar Buffet'),
    ('Completa', 'Completa')
]

ROOM_TYPES = [
    ('No seleccionat', 'No seleccionat'),
    ('Individual', 'Individual'),
    ('Double', 'Double'),
    ('Suite', 'Suite'),
    ('Deluxe', 'Deluxe')
]

CHECK_IN_PATH = {
    1: 'worker/receptionist/check-in/check_in_1.html',
    2: 'worker/receptionist/check-in/check_in_2.html',
    3: 'worker/receptionist/check-in/check_in_3.html',
    4: 'worker/receptionist/check-in/check_in_4.html',

}

RESERVATION_PATH = {
    1: 'worker/receptionist/reservation/new_reservation/new_reservation_1.html',
    2: 'worker/receptionist/reservation/new_reservation/new_reservation_2.html',
    3: 'worker/receptionist/reservation/new_reservation/new_reservation_3.html',
    4: 'worker/receptionist/reservation/new_reservation/new_reservation_4.html',
}

MANAGE_RESERVATION = {
    1: 'worker/receptionist/reservation/manage_reservation/search_reservation.html',
    2: 'worker/receptionist/reservation/manage_reservation/reservation_details.html',
}

CHECK_OUT_PATH = {
    1: 'worker/receptionist/check-out/check_out_1.html',
    2: 'worker/receptionist/check-out/check_out_2.html',
    3: 'worker/receptionist/check-out/check_out_3.html',
    4: 'worker/receptionist/check-out/check_out_4.html',
}

ADMIN_TESTS_PATH = {
    1: 'admin-tests/add_client.html',
    2: 'admin-tests/add_room.html',
}
