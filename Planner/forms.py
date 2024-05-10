from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
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

    def clean(self):
        cleaned_data = super().clean()
        room_num = cleaned_data.get('room_num')
        room_type = cleaned_data.get('room_type')

        try:
            valid_range = c.get_room_number_range(room_type)
            if not valid_range or not (valid_range[0] <= room_num <= valid_range[1]):
                raise ValidationError(f'El número d\'habitació per {room_type} ha de '
                                      f'ser entre {valid_range[0]} i {valid_range[1]}')
        except TypeError:
            raise ValidationError(f'El tipus d\'habitació seleccionat no és vàlid o no està ben configurat')

        if Room.objects.filter(room_num=room_num).exists():
            raise ValidationError('Aquest número d\'habitació ja està en ús')

        return cleaned_data
