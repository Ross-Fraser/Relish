import re
from django import forms
from .models import Product, GRIND_CHOICES, CURRENCY_CHOICES


class PurchaseEnquiryForm(forms.Form):
    product_name = forms.CharField(widget=forms.HiddenInput())
    product_price = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=255)
    contact_number = forms.CharField(max_length=15)
    email_address = forms.EmailField()
    grind = forms.ChoiceField(choices=GRIND_CHOICES)

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if not re.match(r'^\+?\d{10,15}$', contact_number):
            raise forms.ValidationError('Invalid contact number.')
        return contact_number


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category', 'origin', 'grind', 'size', 'manufacturer',
            'name', 'description', 'price', 'currency', 'image'
            ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'origin': forms.Select(attrs={'class': 'form-control'}),
            'grind': forms.Select(attrs={'class': 'form-control'}),
            'size': forms.Select(attrs={'class': 'form-control'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None:
            if price.as_tuple().exponent < -2:
                raise forms.ValidationError("Ensure that the price has no more"
                                            " than 2 decimal places.")

            if price <= 0:
                raise forms.ValidationError('Price must be a positive number.')

            if price > 90:
                raise forms.ValidationError('Price cannot exceed 90.')

        return price
