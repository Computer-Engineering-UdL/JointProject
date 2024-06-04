from django.contrib import admin

from Cleaner.models import CleaningMaterial, Stock, CleanedRoom

admin.site.register(CleaningMaterial)
admin.site.register(Stock)
admin.site.register(CleanedRoom)
