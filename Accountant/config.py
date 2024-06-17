class Config:
    TOURIST_TAX_PER_CLIENT = 3  # €

    @staticmethod
    def get_accountant_home_path():
        return 'worker/accountant/accountant_home.html'

    @staticmethod
    def get_accountant_cleaning_material_path():
        return 'worker/accountant/cleaning_material.html'

    @staticmethod
    def get_accountant_billing_data_path():
        return 'worker/accountant/billing_data.html'
