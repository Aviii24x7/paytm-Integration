from django import forms
from .models import User

class UserForm(forms.ModelForm):
    name=forms.CharField(max_length=20)
    email=forms.EmailField(max_length=54)
    phone=forms.CharField(max_length=13)
    amount=forms.IntegerField()
    
    class Meta:
        exclude=["id", "paid"]
        model=User
    