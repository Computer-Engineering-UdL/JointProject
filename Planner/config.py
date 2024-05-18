class Config:
    @staticmethod
    def get_planner_home_path():
        return 'worker/planner/planner_home.html'

    @staticmethod
    def get_room_assignment_path(n: int):
        return ROOM_ASSIGNMENT_PATHS[n]

    @staticmethod
    def get_new_worker_path():
        return 'worker/planner/new_worker.html'

    @staticmethod
    def get_add_room_path():
        return 'worker/planner/add_room.html'


ROOM_ASSIGNMENT_PATHS = {
    1: 'worker/planner/room_assignment_list.html',
    2: 'worker/planner/room_assignment_detail.html'
}
