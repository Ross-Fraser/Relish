from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_register_view_post_valid_form(self):
        data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

        # Check if the user is created
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_view_post_invalid_form(self):
        # Missing required fields in the form data
        data = {}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username',
                             'This field is required.')
        self.assertFormError(response, 'form', 'password1',
                             'This field is required.')
        self.assertFormError(response, 'form', 'password2',
                             'This field is required.')

    def test_register_view_post_password_mismatch(self):
        # Form submitted with password mismatch
        data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword321',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)

        # Retrieve form from response context
        form = response.context['form']

        # Check if form field 'password2' contains the expected error message
        self.assertIn('The two password fields didn’t match.',
                      form.errors['password2'])

    def test_register_view_authenticated_user(self):
        # Authenticate user
        self.client.force_login(User.objects.create_user
                                (username='existing_user',
                                 password='password123'))
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 302)  # Redirects to home
