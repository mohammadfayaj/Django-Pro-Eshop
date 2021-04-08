from django import forms
from django.forms import ModelForm, Textarea
from .models import Coupon

class CouponForm(forms.ModelForm):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
        'aria-describedby': 'basic-addon2',
        'aria-label': 'Recipient\'s username',
        'placeholder':'Promo code'}))
    class Meta:
        model = Coupon
        fields = ('code',)

class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()

