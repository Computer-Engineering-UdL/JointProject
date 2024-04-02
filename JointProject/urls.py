"""
URL configuration for JointProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from User import views as v


urlpatterns = [
    path('admin-tests/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/signup/", v.signup, name="signup"),
    path('logout/', v.user_logout, name='logout'),
    path('receptionist/', include('Reception.urls')),
    path('worker/', v.worker_home, name='worker_home'),
    path("", v.home, name="base"),
]
