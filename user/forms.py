from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

UserModel = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required. Inform a valid email address.')

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2',)
