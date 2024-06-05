from django import forms
from .models import Order


class OrderCreateForms(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user']
