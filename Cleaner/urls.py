from django.urls import path
from django.views.generic import TemplateView
from Cleaner import views as v

urlpatterns = [
    path("", v.cleaner_home, name="cleaner_home"),
    path("stock/", v.cleaner_stock, name="cleaner_stock"),
    path("rooms/", v.cleaner_cleaned_rooms, name="cleaner_cleaned_rooms"),
    path("rooms/<int:room_id>/", v.cleaner_cleaned_room_info, name="cleaner_cleaned_room_info"),
]
