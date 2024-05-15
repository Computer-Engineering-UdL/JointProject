class Config:

    @staticmethod
    def get_guest_home_path():
        return 'client/client_home.html'

    @staticmethod
    def get_guest_path(n: int):
        return GUEST_PATHS[n]


GUEST_PATHS = {
    1: 'client/room_reservation/new_reservation_step_1.html',
}
