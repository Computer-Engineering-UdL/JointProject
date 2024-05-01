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

    @staticmethod
    def get_material_names():
        return MATERIALS_NAMES


MATERIALS_NAMES = {
    'Esponja': 'esponja.png',
    'Guantes': 'guantes.png',
    'Spray': 'spray.avif',
    'Toalla': 'toalla.avif',
    'Fregasuelos': 'fregasuelos.avif',
    'lejia': 'lejia.avif',
    'limpiacristales': 'limpiacristales.avif',
    'mopa': 'mopa.avif',
    'trapos': 'trapos.avif',
}
