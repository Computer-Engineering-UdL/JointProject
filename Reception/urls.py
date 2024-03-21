from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from user.views import add_client, room_reservation

urlpatterns = [
    path("", TemplateView.as_view(template_name="reception_home.html"), name="home"),
    path('add_client/', add_client, name='add_client'),
    path('room_reservation/', room_reservation, name='room_reservation'),
    ]