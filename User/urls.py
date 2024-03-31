from django.urls import path
from User import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
]
