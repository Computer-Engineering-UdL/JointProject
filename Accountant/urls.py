from django.urls import path

from Accountant import views as v

urlpatterns = [
    path('', v.accountant_home, name='accountant_home'),
    path('billing', v.billing_data, name='billing_data'),
    path('add-new-cleaning-material', v.add_new_cleaning_material, name='add_new_cleaning_material'),
    path('cleaning-material', v.cleaning_material, name='cleaning_material'),

]
