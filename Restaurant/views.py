from django.shortcuts import render
from User.decorators import worker_required
from Restaurant.config import Config as c


@worker_required('restaurant')
def restaurant_home(request):
    return render(request, c.get_restaurant_home_path(1))
