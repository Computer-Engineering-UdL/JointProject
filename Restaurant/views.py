from django.shortcuts import render
from User.decorators import worker_required


@worker_required('restaurant')
def restaurant_home(request):
    return render(request, 'worker/restaurant/restaurant_home.html')
