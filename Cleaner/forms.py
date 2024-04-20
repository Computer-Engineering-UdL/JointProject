from django import forms
from Cleaner.models import Stock, Cleaning_Material


class StockForm(forms.ModelForm):
    material = forms.CharField(label="Introdueix el nom del item a cercar")

    class Meta:
        model = Stock
        fields = ['material']
