from django.urls import path

from Accountant import views as v

urlpatterns = [
    path('', v.accountant_home, name='accountant_home'),
    path('cleaning-material', v.cleaning_material, name='cleaning_material'),
    path('tourist-tax', v.tourist_tax, name='tourist_tax'),
    path('billing', v.billing_data, name='billing_data'),
    path('billing/<int:reservation_id>', v.download_receipt, name='download_receipt'),
    path('add-new-cleaning-material', v.add_new_cleaning_material, name='add_new_cleaning_material'),
    path('cleaning-material', v.cleaning_material, name='cleaning_material'),
    path('send-data-authorities', v.send_guests_data_to_authorities, name='send_guests_data_to_authorities'),
]
