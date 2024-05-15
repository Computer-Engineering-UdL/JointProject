from django.urls import path
from Accountant import views as v


urlpatterns = [
    path('', v.accountant_home, name='accountant_home'),
]
