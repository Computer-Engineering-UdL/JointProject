from django.shortcuts import render
from User.decorators import worker_required


@worker_required('accountant')
def accountant_home(request):
    return render(request, 'worker/accountant/accountant_home.html')


@worker_required('accountant')
def cleaning_material(request):
    return render(request, 'worker/accountant/cleaning_material.html')


@worker_required('accountant')
def billing_data(request):
    return render(request, 'worker/accountant/billing_data.html')
