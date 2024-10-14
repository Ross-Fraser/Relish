import json
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from decimal import Decimal
from bag.models import BagItem
from roastery.models import Product
from checkout.models import Order, OrderLineItem
from profiles.models import UserProfile
from django.contrib.auth.models import User

class CheckoutViewsTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='testuser@example.com'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
        self.bag_item = BagItem.objects.create(
            user=self.user,
            product=Product.objects.create(name='Test Product', price=Decimal('10.00')),
            quantity=1,
        )
        self.url = reverse('checkout')

    @patch('stripe.PaymentIntent.create')
    def test_checkout_view_success(self, mock_create_intent):
        # Mock Stripe payment intent creation
        mock_create_intent.return_value = {
            'id': 'test_intent_id',
            'client_secret': 'test_client_secret'
        }

        response = self.client.get(self.url)

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        self.assertIn('bag_items', response.context)
        self.assertIn('order_form', response.context)
        self.assertIn('client_secret', response.context)
        self.assertEqual(response.context['grand_total'], Decimal('15.00'))

    @patch('stripe.PaymentIntent.modify')
    def test_cache_checkout_data_success(self, mock_modify_intent):
        cache_url = reverse('cache_checkout_data')
        post_data = {
            'client_secret': 'test_intent_id_secret',
            'save_info': 'on',
        }
        response = self.client.post(cache_url, post_data)

        # Check that Stripe intent modification was called
        mock_modify_intent.assert_called_once_with(
            'test_intent_id',
            metadata={
                'bag': json.dumps(self.client.session.get('bag', {})),
                'save_info': 'on',
                'username': self.user.username,
            }
        )
        self.assertEqual(response.status_code, 200)

    @patch('stripe.PaymentIntent.create')
    def test_checkout_success_view(self, mock_create_intent):
        mock_create_intent.return_value = {
            'id': 'test_intent_id',
            'client_secret': 'test_client_secret'
        }

        # Simulate form submission
        post_data = {
            'first_name': 'John',
            'surname': 'Doe',
            'email': 'johndoe@example.com',
            'phone_number': '1234567890',
            'street_address1': '123 Main St',
            'town_or_city': 'Testville',
            'country': 'US',
        }
        response = self.client.post(self.url, post_data)

        # Check order creation and redirection
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Order.objects.filter(user_profile__user=self.user).exists())
        order = Order.objects.get(user_profile__user=self.user)
        self.assertEqual(order.total, Decimal('15.00'))

    def test_checkout_empty_bag_redirect(self):
        # Test redirect when bag is empty
        BagItem.objects.all().delete()
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(
            list(response.context['messages'])[0].message,
            "There's nothing in your bag at the moment"
        )

    def test_checkout_success_view_post_save_info(self):
        # Test successful checkout with 'save_info' option
        profile = UserProfile.objects.create(user=self.user)
        order = Order.objects.create(
            user_profile=profile,
            total=Decimal('20.00'),
            stripe_pid='test_pid',
            original_bag='{"1": {"quantity": 1}}',
        )
        url = reverse('checkout_success', args=[order.order_number])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        self.assertEqual(response.context['order'], order)

        # Ensure the session bag is cleared
        self.assertNotIn('bag', self.client.session)
