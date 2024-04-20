from django import forms
from Cleaner.models import Stock, Cleaning_Material
from Reception.models import Room


class StockForm(forms.ModelForm):
    material = forms.ModelChoiceField(queryset=Cleaning_Material.objects.all(),
                                      label="Introdueix el nom del item a cercar", required=False)

    class Meta:
        model = Stock
        fields = ['material']


class CleanedRoomForm(forms.Form):
    occupied_rooms = forms.ModelChoiceField(queryset=Room.objects.filter(is_taken=True,
                                                                         roomreservation__check_out_active=False),
                                            empty_label="Select a client")

