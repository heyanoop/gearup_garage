from django import forms
from .models import account
import re

class UserRegistration(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password', 'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}))
    
    class Meta:
        model = account
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']
        
    def __init__(self, *args, **kwargs):
        super(UserRegistration, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
           
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last_name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone_number'

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.strip().startswith(' ') and not re.match("^[a-zA-Z]*$", first_name):
            raise forms.ValidationError('First name should contain only alphabets and should not start with a space')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.strip().startswith(' ') and not re.match("^[a-zA-Z]*$", last_name):
            raise forms.ValidationError('Last name should contain only alphabets and should not start with a space')
        return last_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise forms.ValidationError('Phone number should contain only digits')
        elif account.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('Mobile number already exists')
        return phone_number
    
    def clean(self):
        cleaned_data = super(UserRegistration, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
