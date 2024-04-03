class Config:
    @staticmethod
    def get_room_extra_costs():
        return Config.room_extra_costs

    @staticmethod
    def get_room_type_costs():
        return Config.room_type_costs

    room_extra_costs = {
        'Minibar': [10],
        'Desperfectes': [20],
        'Servei habitacions': [15],
        'Pàrquing': [5],
        'Pèrdua de claus': [20]
    }

    room_type_costs = {
        'Individual': [50],
        'Double': [75],
        'Suite': [100],
        'Deluxe': [125]
    }
