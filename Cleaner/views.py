from django.shortcuts import render
from Cleaner.forms import StockForm
from Cleaner.models import Stock
from User.decorators import worker_required
from Cleaner.config import Config as c


@worker_required('cleaner')
def cleaner_home(request):
    return render(request, 'worker/cleaner/cleaner_home.html')


@worker_required('cleaner')
def cleaner_stock(request):
    form = StockForm()
    stock = Stock.objects.filter(is_active=True)
    return render(request, c.get_cleaner_stock_path(1), {'form': form, 'stock': stock})
