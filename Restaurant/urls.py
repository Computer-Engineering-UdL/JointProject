from django.urls import path
from django.views.generic import TemplateView
from Restaurant import views as v

urlpatterns = [
    path("", v.restaurant_home, name="cleaner_home"),
]
