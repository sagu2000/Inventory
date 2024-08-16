
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'sku', 'price', 'quantity']


class RestockForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())     
    amount = forms.IntegerField(min_value=1)

class SaleForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    amount = forms.IntegerField(min_value=1)
