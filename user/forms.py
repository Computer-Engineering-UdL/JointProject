from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

UserModel = get_user_model()


class SignUpForm(UserCreationForm):
    FirstName = forms.CharField(max_length=80, help_text='Required. Inform your first name.')
    LastName = forms.CharField(max_length=80, help_text='Required. Inform your last name.')
    PhoneNumber = forms.CharField(max_length=12, label='Phone Number', help_text='Required. Inform your phone number.')
    IDNumber = forms.CharField(max_length=20, label='DNI, NIE or Passport', help_text='Required. Inform your ID number.')
    email = forms.EmailField(max_length=100, help_text='Required. Inform a valid email address.')

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2',)
