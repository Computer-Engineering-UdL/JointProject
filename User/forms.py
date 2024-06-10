from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from User.validators import is_valid_id_number, is_valid_phone

UserModel = get_user_model()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=80, label='Nom',
                                 error_messages={'required': 'Introdueix el teu nom'})
    last_name = forms.CharField(max_length=80, label='Cognoms',
                                error_messages={'required': 'Introdueix el teu cognom'})
    phone_number = forms.CharField(max_length=9, label='Número de telèfon',
                                   error_messages={'required': 'El número de telefon no és vàlid'})

    id_number = forms.CharField(max_length=20,
                                required=False,
                                label='Número d\'identificació',
                                error_messages={'invalid': 'El número d\'identificació no és vàlid'})

    email = forms.EmailField(max_length=100, label='Correu electrònic',
                             error_messages={'required': 'Obligatori. Informeu una adreça de correu electrònic vàlida',
                                             'invalid': 'El correu no és valid'})

    password1 = forms.CharField(max_length=100, label='Contrasenya',
                                widget=forms.PasswordInput,
                                error_messages={'required': 'Introdueix una contrasenya'})

    password2 = forms.CharField(max_length=100, label='Confirma la contrasenya',
                                widget=forms.PasswordInput,
                                error_messages={'required': 'Confirma la contrasenya'})

    def clean_id_number(self):
        """Check if the ID number provided is valid."""
        id_number = self.cleaned_data.get('id_number')
        if id_number:
            if is_valid_id_number(id_number):
                return id_number
            else:
                raise ValidationError("Número d'identificació no vàlid. "
                                      "Introduïu un DNI, NIE o número de passaport vàlid")

        return id_number

    def clean_phone_number(self):
        """Check if the phone number provided is valid."""
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            if is_valid_phone(phone_number):
                return phone_number
            else:
                raise ValidationError('Número de telèfon no vàlid. Introdueix un número de telèfon vàlid')

        return phone_number

    class Meta:
        model = UserModel
        fields = ('username', 'id_number', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number')


class PopulateForm(forms.Form):
    CHOICES = (
        ('users', 'Create Users'),
        ('workers', 'Populate Workers'),
        ('clients', 'Populate Clients'),
        ('rooms', 'Populate Rooms'),
        ('reservations', 'Populate Reservations'),
        ('materials', 'Create Cleaning Materials'),
        ('stock', 'Populate Stock'),
        ('cleaned_rooms', 'Populate Cleaned Rooms'),
        ('external_clients', 'Populate External Clients'),
        ('restaurant_reservations', 'Populate Restaurant Reservations'),
        ('expenses', 'Populate Expenses'),
        ('extra_costs', 'Populate Extra Costs'),
    )

    data_type = forms.ChoiceField(choices=CHOICES, label="Select data type to populate")
    entries = forms.IntegerField(min_value=1, max_value=100, initial=10, label="Number of entries")
