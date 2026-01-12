from django import forms
from .models import CustomUser, Order, DepositRequest
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','username','email', 'phone_number','tg_username','avatar']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','username','email','tg_username','phone_number','avatar']



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address', 'phone', 'email', 'tg_username']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'address': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'phone': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'value': '+998'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded'}),
            'tg_username': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
        }


class DepositRequestForm(forms.ModelForm):
    class Meta:
        model = DepositRequest
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter a amount (so\'m)','min': '10000','step': '1000'})
        }