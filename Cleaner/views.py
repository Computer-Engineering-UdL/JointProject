from django.shortcuts import render
from User.decorators import worker_required


@worker_required('cleaner')
def cleaner_home(request):
    return render(request, 'worker/cleaner/cleaner_home.html')
