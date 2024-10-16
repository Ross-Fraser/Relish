from django.test import TestCase
from .forms import OrderForm
from .models import Order

class TestOrderForm(TestCase):

    def test_order_form_valid_data(self):
        form = OrderForm(data={
            'first_name': 'John',
            'surname': 'Doe',
            'email': 'john.doe@example.com',
            'phone_number': '123456789',
            'street_address1': '123 Main St',
            'street_address2': '',
            'town_or_city': 'Anytown',
            'county': 'Anycounty',
            'postcode': '12345',
            'country': 'US',
        })
        self.assertTrue(form.is_valid())

    def test_order_form_missing_required_fields(self):
        form = OrderForm(data={
            'surname': 'Doe',
            'email': 'john.doe@example.com',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('phone_number', form.errors)
        self.assertIn('street_address1', form.errors)
        self.assertIn('town_or_city', form.errors)
        self.assertIn('country', form.errors)

    def test_order_form_field_placeholders(self):
        form = OrderForm()
        self.assertEqual(form.fields['first_name'].widget.attrs['placeholder'], 'First Name *')
        self.assertEqual(form.fields['surname'].widget.attrs['placeholder'], 'Surname *')
        self.assertEqual(form.fields['email'].widget.attrs['placeholder'], 'Email Address *')

    def test_order_form_autofocus_field(self):
        form = OrderForm()
        self.assertTrue(form.fields['surname'].widget.attrs['autofocus'])

    def test_order_form_css_class(self):
        form = OrderForm()
        for field in form.fields:
            self.assertEqual(form.fields[field].widget.attrs['class'], 'stripe-style-input')

