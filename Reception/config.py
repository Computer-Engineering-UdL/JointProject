class Config:
    @staticmethod
    def get_room_extra_costs():
        return Config.room_extra_costs

    room_extra_costs = [
        ('Minibar', 'Minibar'),
        ('Desperfectes', 'Desperfectes'),
        ('Servei habitacions', 'Servei habitacions'),
        ('Parking', 'Parking'),
        ('Perdua de claus', 'Perdua de claus'),
    ]
