from django import forms
from Cleaner.models import Stock, Cleaning_Material


class StockForm(forms.ModelForm):
    material = forms.ModelChoiceField(queryset=Cleaning_Material.objects.all(),
                                      label="", required=False)

    class Meta:
        model = Stock
        fields = ['material']
