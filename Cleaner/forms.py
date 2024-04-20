from django import forms
from Cleaner.models import Stock, Cleaning_Material, CleanedRoom
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
    missing_objects = forms.CharField(label="S'han deixat alguna cosa?", required=False)
    need_towels = forms.IntegerField(label="Falten tovalloles?", required=False)
    additional_comments = forms.CharField(label="Comentaris addicionals", required=False)

    class Meta:
        model = CleanedRoom
        fields = ['occupied_rooms', 'missing_objects', 'need_towels', 'additional_comments']
