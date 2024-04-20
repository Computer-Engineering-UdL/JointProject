from django.urls import path
from django.views.generic import TemplateView
from Cleaner import views as v

urlpatterns = [
    path("", v.cleaner_home, name="cleaner_home"),
]
