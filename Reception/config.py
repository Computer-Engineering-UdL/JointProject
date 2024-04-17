from Reception.paths import Path as p


class Config:
    ID_NUMBER = 20
    DROPDOWN_MAX_LENGTH = 15
    TEXT_SIZE = 120
    PHONE_NUMBER_LENGTH = 9
    RECEIPT_CHECKIN_FILENAME = 'receipt_checkin.pdf'
    RECEIPT_CHECKOUT_FILENAME = 'receipt_checkout.pdf'

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
    def get_room_prices_per_type():
        return ROOM_PRICES_PER_TYPE

    @staticmethod
    def get_check_in_path(n: int):
        return p.CHECK_IN_PATH[n]

    @staticmethod
    def get_reservation_path(n: int):
        return p.RESERVATION_PATH[n]

    @staticmethod
    def get_manage_reservation_path(n: int):
        return p.MANAGE_RESERVATION[n]

    @staticmethod
    def get_check_out_path(n: int):
        return p.CHECK_OUT_PATH[n]

    @staticmethod
    def get_admin_tests_path(n: int):
        return p.ADMIN_TESTS_PATH[n]


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

ROOM_PRICES_PER_TYPE = [
    ('No seleccionat', 0),
    ('Individual', 50),
    ('Double', 75),
    ('Suite', 100),
    ('Deluxe', 125)
]
