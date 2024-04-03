class Config:
    @staticmethod
    def get_room_extra_costs():
        return room_extra_costs

    @staticmethod
    def get_check_in_path(n: int):
        return check_in_path[n]

    @staticmethod
    def get_reservation_path(n: int):
        return reservation_path[n]

    @staticmethod
    def get_manage_reservation_path(n: int):
        return manage_reservation[n]

    @staticmethod
    def get_check_out_path(n: int):
        return check_out_path[n]

    @staticmethod
    def get_admin_tests_path(n: int):
        return admin_tests_path[n]


room_extra_costs = [
    ('Minibar', 'Minibar'),
    ('Desperfectes', 'Desperfectes'),
    ('Servei habitacions', 'Servei habitacions'),
    ('Parking', 'Parking'),
    ('Perdua de claus', 'Perdua de claus'),
]

check_in_path = {
    1: 'worker/receptionist/check-in/check_in_1.html',
    2: 'worker/receptionist/check-in/check_in_2.html',
    3: 'worker/receptionist/check-in/check_in_3.html',
    4: 'worker/receptionist/check-in/check_in_4.html',

}

reservation_path = {
    1: 'worker/receptionist/reservation/new_reservation/new_reservation_1.html',
    2: 'worker/receptionist/reservation/new_reservation/new_reservation_2.html',
    3: 'worker/receptionist/reservation/new_reservation/new_reservation_3.html',
    4: 'worker/receptionist/reservation/new_reservation/new_reservation_4.html',
}

manage_reservation = {
    1: 'worker/receptionist/reservation/manage_reservation/search_reservation.html',
    2: 'worker/receptionist/reservation/manage_reservation/reservation_details.html',
}

check_out_path = {
    1: 'worker/receptionist/check-out/check_out_1.html',
    2: 'worker/receptionist/check-out/check_out_2.html',
    3: 'worker/receptionist/check-out/check_out_3.html',
    4: 'worker/receptionist/check-out/check_out_4.html',
}

admin_tests_path = {
    1: 'admin-tests/add_client.html',
    2: 'admin-tests/add_room.html',
}
