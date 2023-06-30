from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models  import  AddProduct,Orders

class AdminLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class SignupForm(UserCreationForm):
   

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    
    
class PostForm(forms.ModelForm):
    class Meta:
        model = AddProduct
        fields = ['name','price','description','quantity','image']

class AddressForm(forms.Form):
    
    Mobile= forms.IntegerField()
    Address = forms.CharField(max_length=500)
        
class OrderForm(forms.ModelForm):
    class Meta:
        model=Orders
        fields=['status']
