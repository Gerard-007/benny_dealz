from django import forms
from django.forms import NumberInput


class WalletForm(forms.Form):
    bvn = forms.CharField(widget=NumberInput(attrs={'class':'form-control', 'placeholder':'Your BVN', 'required':'required'}))
