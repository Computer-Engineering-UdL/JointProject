from django.contrib import messages
from django.shortcuts import render, redirect

from Cleaner.models import Stock
from User.decorators import worker_required
from Cleaner.forms import StockForm, AddNewCleningMaterialForm


@worker_required('accountant')
def accountant_home(request):
    return render(request, 'worker/accountant/accountant_home.html')


@worker_required('accountant')
def cleaning_material(request):
    form = StockForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            material_name = form.cleaned_data.get('material')
            if material_name:
                stock = Stock.objects.filter(material__material_name__icontains=material_name, is_active=True)
            else:
                stock = Stock.objects.filter(is_active=True)

            if 'update_stock' in request.POST:
                submitted_stock_ids = set(map(int, request.POST.getlist('stock[]')))
                all_active_stocks = set(Stock.objects.filter(is_active=True).values_list('id', flat=True))

                for stock_id in all_active_stocks:
                    item = Stock.objects.get(id=stock_id)
                    item.is_available = stock_id not in submitted_stock_ids
                    item.save()
                messages.success(request, 'Stock actualitzat correctament')

                return redirect('cleaner_stock')
        else:
            stock = Stock.objects.filter(is_active=True)
    else:
        stock = Stock.objects.filter(is_active=True)

    return render(request, 'worker/accountant/cleaning_material.html', {'form': form, 'stock': stock})



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
