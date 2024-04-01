from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from User.validators import is_valid_id_number, is_valid_phone

UserModel = get_user_model()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=80,
                                 error_messages={'required': 'Required. Inform your first name.'})
    last_name = forms.CharField(max_length=80,
                                error_messages={'required': 'Required. Inform your last name.'})
    phone_number = forms.CharField(max_length=9, label='Phone Number',
                                   error_messages={'required': 'Required. Select your ID type.'})

    id_number = forms.CharField(max_length=20,
                                required=False,
                                label='ID Number',
                                error_messages={'invalid': 'Invalid ID number.'})

    email = forms.EmailField(max_length=100,
                             error_messages={'required': 'Required. Inform a valid email address.',
                                             'invalid': 'Invalid email address.'})

    def clean_id_number(self):
        """Check if the ID number provided is valid."""
        id_number = self.cleaned_data.get('id_number')
        if id_number:
            if is_valid_id_number(id_number):
                return id_number
            else:
                raise ValidationError('Invalid ID number. Please enter a valid DNI, NIE, or Passport number.')

        return id_number

    def clean_phone_number(self):
        """Check if the phone number provided is valid."""
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            if is_valid_phone(phone_number):
                return phone_number
            else:
                raise ValidationError('Invalid phone number. Please enter a valid phone number.')

        return phone_number

    class Meta:
        model = UserModel
        fields = ('username', 'id_number', 'email', 'password1', 'password2',)
