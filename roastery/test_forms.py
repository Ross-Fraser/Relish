from decimal import Decimal
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django import forms  # Import the forms module from Django
import os
from .forms import PurchaseEnquiryForm, ProductForm
from .models import GRIND_CHOICES, Category, CoffeeOrigin, \
CoffeeGrind, CoffeeSize


class PurchaseEnquiryFormTest(TestCase):

    def test_valid_form(self):
        form_data = {
            'product_name': (widget := forms.HiddenInput()),
            'product_price': (widget := forms.HiddenInput()),
            'name': 'John Doe',
            'address': '123 Main St',
            'contact_number': '+1234567890',
            'email_address': 'john.doe@example.com',
            'grind': GRIND_CHOICES[0][0]
        }
        form = PurchaseEnquiryForm(data=form_data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

    def test_invalid_contact_number(self):
        form_data = {
            'product_name': 'Coffee',
            'product_price': '10.00',
            'name': 'John Doe',
            'address': '123 Main St',
            'contact_number': '123456',  # invalid phone number
            'email_address': 'john.doe@example.com',
            'grind': GRIND_CHOICES[0][0]
        }
        form = PurchaseEnquiryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('contact_number', form.errors)

    def test_missing_required_fields(self):
        form_data = {
            'product_name': 'Coffee',
            'product_price': '10.00',
            'name': 'John Doe',
            # Missing address, contact_number, email_address, and grind
        }
        form = PurchaseEnquiryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('address', form.errors)
        self.assertIn('contact_number', form.errors)
        self.assertIn('email_address', form.errors)
        self.assertIn('grind', form.errors)


class ProductFormTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(main_category='Arabica')
        self.origin = CoffeeOrigin.objects.create(continent=0, country=1,
                                                  region=1)
        self.grind = CoffeeGrind.objects.create(grind=3)
        self.size = CoffeeSize.objects.create(size=250, unit='Gramm')

    def test_valid_form_with_image(self):
        # Get the absolute path to the image file
        image_path = os.path.join('static', 'images', 'coffee',
                                  'relish_test_image.webp')

        # Open the image file in binary mode and read its content
        with open(image_path, 'rb') as f:
            file_content = f.read()

        # Create a temporary image file for testing
        image_file = SimpleUploadedFile('relish_test_image.webp',
                                        file_content,
                                        content_type='image/webp')

        # Populate form data including the image field with the temporary image
        form_data = {
            'category': self.category,
            'origin': self.origin,
            'grind': self.grind,
            'size': self.size,
            'manufacturer': 'Relish',
            'name': 'Premium Coffee',
            'description': 'The best coffee in town.',
            "price": Decimal("7.54"),
            'currency': 'USD',
        }
        form = ProductForm(data=form_data, files={'image': image_file})
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

    def test_invalid_price(self):
        image_path = os.path.join('static', 'images', 'coffee',
                                  'relish_test_image.webp')

        with open(image_path, 'rb') as f:
            file_content = f.read()

        image_file = SimpleUploadedFile('relish_test_image.webp', file_content,
                                        content_type='image/webp')

        form_data = {
            'category': self.category,
            'origin': self.origin,
            'grind': self.grind,
            'size': self.size,
            'manufacturer': 'Relish',
            'name': 'Premium Coffee',
            'description': 'The best coffee in town.',
            'price': Decimal('invalid-price'),
            'currency': 'USD',
        }
        form = ProductForm(data=form_data, files={'image': image_file})
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)

    def test_missing_required_fields(self):
        form_data = {
            'category': self.category,
            'origin': self.origin,
            # Missing grind, size, manufacturer, name, description,
            # price, currency, and image
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('grind', form.errors)
        self.assertIn('size', form.errors)
        self.assertIn('manufacturer', form.errors)
        self.assertIn('name', form.errors)
        self.assertIn('description', form.errors)
        self.assertIn('price', form.errors)
        self.assertIn('currency', form.errors)
