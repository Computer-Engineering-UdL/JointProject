from django import forms
from django.core.exceptions import ValidationError

from Cleaner.models import Stock, CleaningMaterial, CleanedRoom
from Cleaner.forms_verify import verify_new_material


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

class AddNewCleningMaterialForm(forms.ModelForm):

    material_name = forms.CharField(label='Nom del material', required=True)
    image = forms.ImageField(label='Imatge del material', required=True)
    class Meta:
        model = CleaningMaterial
        fields = ['material_name', 'image']
        labels = {
            'material_name': 'Nombre del material',
            'image': 'Imagen del material'
        }

    def clean(self):
        cleaned_data = super().clean()
        material_name = cleaned_data.get('material_name')

        try:
            verify_new_material(material_name)
        except ValidationError as e:
            self.add_error(None, e)
