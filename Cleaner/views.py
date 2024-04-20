from django.shortcuts import render, redirect
from Cleaner.forms import StockForm
from Cleaner.models import Stock
from User.decorators import worker_required
from Cleaner.config import Config as c


@worker_required('cleaner')
def cleaner_home(request):
    return render(request, 'worker/cleaner/cleaner_home.html')


@worker_required('cleaner')
def cleaner_stock(request):
    form = StockForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            material_name = form.cleaned_data.get('material')
            if material_name:
                stock = Stock.objects.filter(material__material_name__icontains=material_name, is_active=True)
            else:
                stock = Stock.objects.filter(is_active=True)
            if 'update_stock' in request.POST:
                stock_ids = request.POST.getlist('stock[]')
                for stock_id in stock_ids:
                    item = Stock.objects.get(id=stock_id)
                    item.is_available = not item.is_available
                    item.save()
                return redirect('cleaner_stock')
        else:
            stock = Stock.objects.filter(is_active=True)
    else:
        stock = Stock.objects.filter(is_active=True)

    return render(request, c.get_cleaner_stock_path(1), {'form': form, 'stock': stock})
