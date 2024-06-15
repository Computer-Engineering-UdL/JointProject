from django import forms
from django.db.models import Sum
from Cleaner.models import CleaningMaterial


def verify_new_material(material_name):
    if CleaningMaterial.objects.filter(material_name=material_name).exists():
        raise forms.ValidationError("El material ja existeix")
