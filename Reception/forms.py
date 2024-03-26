from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Subquery

from .models import RoomReservation, Client, Room


class RoomForm(forms.ModelForm):
    is_clean = forms.BooleanField(required=False)
    is_taken = forms.BooleanField(required=False)
    room_num = forms.IntegerField(validators=[MinValueValidator(200), MaxValueValidator(499)])
    room_price = forms.IntegerField(validators=[MinValueValidator(20), MaxValueValidator(1000)])
    room_type = forms.ChoiceField(choices=Room.ROOM_TYPES)

    class Meta:
        model = Room
        fields = ['room_num', 'room_price', 'room_type', 'is_clean', 'is_taken']


class RoomReservationForm(forms.ModelForm):

    check_in = forms.DateField(input_formats=['%d/%m/%Y'])
    check_out = forms.DateField(input_formats=['%d/%m/%Y'])
    pension_type = forms.ChoiceField(choices=RoomReservation.PENSION_TYPES)
    num_guests = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    room_type = forms.ChoiceField(choices=Room.ROOM_TYPES)
    room = forms.ChoiceField()
    client = forms.ModelChoiceField(queryset=Client.objects.all(), empty_label="Select a client")

    def __init__(self, *args, **kwargs):
        super(RoomReservationForm, self).__init__(*args, **kwargs)
        self.fields['room'].choices = [(room.id, room.room_num) for room in Room.objects.all()]

    def clean_room(self):
        room_id = self.cleaned_data.get('room')
        try:
            room_id = int(room_id)
        except ValueError:
            raise forms.ValidationError("Invalid room id.")
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            raise forms.ValidationError("Room with given id does not exist.")
        return room

    class Meta:
        model = RoomReservation
        fields = ['check_in', 'check_out', 'pension_type', 'num_guests', 'room_type', 'room', 'client']


class AddClientForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    dni = forms.CharField(max_length=9)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=9)
    is_hosted = forms.BooleanField(required=False)

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'dni', 'email', 'phone_number', 'is_hosted']
