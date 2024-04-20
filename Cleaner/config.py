from Cleaner.paths import Path as p


class Config:
    @staticmethod
    def get_cleaner_home_path(n: int):
        return p.CLEANER_ROOMS_PATH[n]

    @staticmethod
    def get_cleaner_stock_path(n: int):
        return p.CLEANER_STOCK_PATH[n]

    @staticmethod
    def get_cleaner_rooms_path(n: int):
        return p.CLEANER_ROOMS_PATH[n]
