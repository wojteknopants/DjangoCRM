from django.forms import ModelForm, TextInput, EmailInput, PasswordInput, CharField
from .models import Order, Customer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    #for styling input fields to class: form-control
    def __init__(self, *args, **kwargs):
            super(CreateUserForm, self).__init__(*args, **kwargs)

            for field in self.fields:
                self.fields[field].widget.attrs.update({'class': 'form-control'})
        