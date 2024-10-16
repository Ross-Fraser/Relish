from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from profiles.models import UserProfile
from checkout.models import Order

class ProfileViewTest(TestCase):

    def setUp(self):
        # Create a test user and profile
        self.user = User.objects.create_user(username='testuser', password='password')
        self.profile = UserProfile.objects.create(user=self.user)
        self.client.login(username='testuser', password='password')

    def test_profile_view_get(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
        self.assertTrue('form' in response.context)
        self.assertTrue('orders' in response.context)
        self.assertTrue(response.context['on_profile_page'])

    def test_profile_view_post_valid_data(self):
        response = self.client.post(reverse('profile'), {
            'default_phone_number': '123456789',
            'default_country': 'US',
        })
        self.profile.refresh_from_db()
        messages = list(get_messages(response.wsgi_request))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.profile.default_phone_number, '123456789')
        self.assertEqual(str(messages[0]), 'Profile updated successfully')

    def test_profile_view_post_invalid_data(self):
        response = self.client.post(reverse('profile'), {
            'default_phone_number': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'default_phone_number', 'This field is required.')


class OrderHistoryViewTest(TestCase):

    def setUp(self):
        # Create a test user and order
        self.user = User.objects.create_user(username='testuser', password='password')
        self.profile = UserProfile.objects.create(user=self.user)
        self.order = Order.objects.create(user_profile=self.profile, order_number='123456')
        self.client.login(username='testuser', password='password')

    def test_order_history_view_get(self):
        response = self.client.get(reverse('order_history', args=['123456']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        self.assertEqual(response.context['order'], self.order)
        self.assertTrue(response.context['from_profile'])

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'This is a past confirmation for order number 123456. A confirmation email was sent on the order date.')
