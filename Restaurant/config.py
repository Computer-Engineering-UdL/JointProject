from Restaurant.paths import Path as p


class Config:
    @staticmethod
    def get_restaurant_home_path(n: int):
        return p.RESTAURANT_HOME_PATH[n]

    @staticmethod
    def get_restaurant_new_reservation_path(n: int):
        return p.RESTAURANT_NEW_RESERVATION_PATH[n]

    @staticmethod
    def get_restaurant_check_reservations_path(n: int):
        return p.RESTAURANT_CHECK_RESERVATIONS_PATH[n]
