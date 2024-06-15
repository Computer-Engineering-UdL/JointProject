from django.contrib import messages
from django.shortcuts import render, redirect

from User.decorators import worker_required
from Cleaner.forms import StockForm, AddNewCleningMaterialForm


@worker_required('accountant')
def accountant_home(request):
    return render(request, 'worker/accountant/accountant_home.html')


@worker_required('accountant')
def cleaning_material(request):
    return render(request, 'worker/accountant/cleaning_material.html')


@worker_required('accountant')
def add_new_cleaning_material(request):
    if request.method == 'POST':
        form = AddNewCleningMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "S'ha creat el nou material amb èxit!")
            return redirect('accountant_home')
    else:
        form = AddNewCleningMaterialForm()
    return render(request, 'worker/accountant/new_cleaning_material.html', {'form': form})


@worker_required('accountant')
def billing_data(request):
    return render(request, 'worker/accountant/billing_data.html')
