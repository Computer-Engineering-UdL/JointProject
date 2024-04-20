from django import forms
from Cleaner.models import Stock, Cleaning_Material


class StockForm(forms.ModelForm):
    material = forms.ModelChoiceField(queryset=Cleaning_Material.objects.all(),
                                      label="Introdueix el nom del item a cercar", required=False)

    class Meta:
        model = Stock
        fields = ['material']
