from django import forms

from Cleaner.models import Stock, CleaningMaterial, CleanedRoom


class StockForm(forms.ModelForm):
    material = forms.ModelChoiceField(queryset=CleaningMaterial.objects.all(),
                                      label="", required=False, empty_label="Selecciona un material")

    class Meta:
        model = Stock
        fields = ['material']


class CleanedRoomForm(forms.Form):
    missing_objects = forms.CharField(required=False)
    need_towels = forms.IntegerField(required=False)
    additional_comments = forms.CharField(required=False)

    class Meta:
        model = CleanedRoom
        fields = ['missing_objects', 'need_towels', 'additional_comments']
