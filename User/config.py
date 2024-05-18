class Config:

    @staticmethod
    def get_worker_type_to_url():
        return {
            'receptionist': 'receptionist_home',
            'cleaner': 'cleaner_home',
            'restaurant': 'restaurant_home',
            'accountant': 'accountant_home',
            'planner': 'planner_home'
        }
