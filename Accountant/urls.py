from django.urls import path

from Accountant import views as v

urlpatterns = [
    path('', v.accountant_home, name='accountant_home'),
    path('cleaning-material', v.cleaning_material, name='cleaning_material'),
    path('billing', v.billing_data, name='billing_data'),
]
