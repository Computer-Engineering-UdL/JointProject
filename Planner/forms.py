from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from Reception.models import Room
from Reception.config import Config as c


class RoomForm(forms.ModelForm):
    is_clean = forms.BooleanField(required=False)
    is_taken = forms.BooleanField(required=False)
    room_num = forms.IntegerField(validators=[MinValueValidator(200), MaxValueValidator(499)])
    room_type = forms.ChoiceField(choices=c.get_room_types)

    class Meta:
        model = Room
        fields = ['room_num', 'room_type', 'is_clean', 'is_taken']
