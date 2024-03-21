from django import forms
from .models import RoomReservation, Client


class RoomReservationForm(forms.ModelForm):
    class Meta:
        model = RoomReservation
        fields = ['check_in', 'check_out', 'pension_type', 'num_guests']


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

    def __init__(self, *args, **kwargs):
        super(AddClientForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['dni'].initial = self.instance.user.dni
            self.fields['email'].initial = self.instance.user.email
            self.fields['phone_number'].initial = self.instance.user.phone_number
            self.fields['is_hosted'].initial = self.instance.is_hosted

    def save(self, commit=True):
        instance = super(AddClientForm, self).save(commit=False)
        user = instance.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.dni = self.cleaned_data['dni']
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        instance.is_hosted = self.cleaned_data['is_hosted']
        if commit:
            user.save()
            instance.save()
        return instance
