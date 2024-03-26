from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

UserModel = get_user_model()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=80, required=True,
                                 error_messages={'required': 'Required. Inform your first name.'})
    last_name = forms.CharField(max_length=80, required=True,
                                error_messages={'required': 'Required. Inform your last name.'})
    phone_number = forms.CharField(max_length=9, required=True, label='Phone Number',
                                   error_messages={'required': 'Required. Select your ID type.'})

    ID_TYPE_CHOICES = [
        ('DNI', 'DNI'),
        ('NIE', 'NIE'),
        ('Passport', 'Passport'),
    ]

    id_type = forms.ChoiceField(choices=ID_TYPE_CHOICES, label='ID Type',
                                error_messages={'required': 'Required. Select your ID type.'})

    # TODO: Validate the ID number (length and constraints) depending on the ID type

    id_number = forms.CharField(max_length=20,
                                required=False,
                                label='ID Number',
                                error_messages={'required': 'Required. Inform your ID number.'})

    email = forms.EmailField(max_length=100, required=True,
                             error_messages={'required': 'Required. Inform a valid email address.',
                                             'invalid': 'Invalid email address.'})

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2',)
