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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from User import views as v

urlpatterns = [
    path('admin-tests/', admin.site.urls),
    path("accounts/signup/", v.signup, name="signup"),
    path("accounts/login/", v.login_custom, name="login"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('logout/', v.user_logout, name='logout'),
    path('receptionist/', include('Reception.urls')),
    path('cleaner/', include('Cleaner.urls')),
    path('restaurant/', include('Restaurant.urls')),
    path('accountant/', include('Accountant.urls')),
    path('planner/', include('Planner.urls')),
    path('guest/', include('Guest.urls')),
    path('populate/', v.populate, name='populate'),
    path("", v.home, name="base"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
