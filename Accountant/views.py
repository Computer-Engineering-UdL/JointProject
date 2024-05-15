from django.shortcuts import render
from User.decorators import worker_required


@worker_required('accountant')
def accountant_home(request):
    return render(request, 'worker/accountant/accountant_home.html')
