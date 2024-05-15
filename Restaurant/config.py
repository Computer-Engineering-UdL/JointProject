from Restaurant.paths import Path as p


class Config:
    MAX_GUESTS_PER_DAY = 25
    MAX_GUESTS_PER_RESERVATION = 25
    MAX_RESERVATION_YEAR_AHEAD = 1

    @staticmethod
    def get_restaurant_home_path():
        return p.RESTAURANT_HOME_PATH

    @staticmethod
    def get_restaurant_new_reservation_path(n: int):
        return p.RESTAURANT_NEW_RESERVATION_PATH[n]

    @staticmethod
    def get_restaurant_check_reservations_path(n: int):
        return p.RESTAURANT_CHECK_RESERVATIONS_PATH[n]

    @staticmethod
    def get_restaurant_services():
        return RESTAURANT_SERVICES


RESTAURANT_SERVICES = [
    ('Esmorzar', 'Esmorzar'),
    ('Dinar', 'Dinar'),
    ('Sopar', 'Sopar')
]
