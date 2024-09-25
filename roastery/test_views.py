from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from roastery.models import Category, Product, CoffeeOrigin, CoffeeGrind,CoffeeSize


class ProductViewTests(TestCase):

    def setUp(self):
        # Create a test user with necessary permissions
        self.user = User.objects.create_user(username='testuser',
                                             password='password')
        self.add_permission = Permission.objects.get(codename='add_product')
        self.change_permission = Permission.objects.get(codename='change_product')
        self.delete_permission = Permission.objects.get(codename='delete_product')
        self.user.user_permissions.add(self.add_permission,
                                       self.change_permission,
                                       self.delete_permission),
        self.client.login(username='testuser', password='password')

        # Create test product
        self.category = Category.objects.create(
            category_id=0,
            main_category="Test Category"
        )
        self.origin = CoffeeOrigin.objects.create(continent="0",
                                                     country="1",
                                                     region="1")
        self.grind = CoffeeGrind.objects.create(grind="3")
        self.size = CoffeeSize.objects.create(size="200", unit="Test Unit")
        self.product = Product.objects.create(
            product=10,
            category=self.category,
            origin=self.origin,
            grind=self.grind,
            size=self.size,
            manufacturer='Relish',
            name='Premium Coffee',
            description='The best coffee in town.',
            price=Decimal('7.54'),
            currency='GBP',
            image="",
        )

        if not self.product.product_id:
            raise ValueError("Product ID is not set correctly.")

    def test_create_product_view_get(self):
        response = self.client.get(reverse('create_product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'roastery/product_form.html')

        form_data = {
            "product_id": 2,
            "category": 1,
            "origin": 1,
            "grind": 2,
            "size": 0,
            "manufacturer": "Relish",
            "name": "Premium Coffee",
            "description": "The best coffee in town.",
            "price": Decimal("-7.54"),
            "currency": "GBP",
            "image": ""
        }

        response = self.client.post(reverse('create_product'), data=form_data,
                                    format='multipart')
        self.assertRedirects(response, reverse('manage_products') +
                             '?success_message=Product created successfully!')

    def test_update_product_view_get(self):
        response = self.client.get(reverse('update_product',
                                           args=[self.product.product_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'roastery/product_form.html')

    def test_update_product_view_post(self):
        form_data = {
            "name": "Updated Product",
            "price": Decimal("10.99"),
        }
        # Ensure the product exists before updating
        self.assertTrue(Product.objects.filter(
            product_id=self.product.product_id).exists())
        response = self.client.post(reverse('update_product',
                                    kwargs={'product_id':
                                            self.product.product_id}),
                                    data=form_data)
        self.assertRedirects(response, reverse('manage_products') +
                             '?success_message=Product updated successfully!')

    def test_delete_product_view_post(self):
        response = self.client.post(reverse('delete_product',
                                    args=[self.product.product_id]))

        # Check if the product is deleted
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(product_id=self.product.product_id)

        # Ensure it redirects to the correct URL
        self.assertRedirects(response, f'{reverse("manage_products")}?'
                                       f'success_message=Product'
                                       f' deleted successfully!')

    def test_delete_product_view_without_login(self):
        self.client.logout()
        response = self.client.post(reverse('delete_product',
                                    args=[self.product.product_id]))
        self.assertRedirects(
            response,
            f'{reverse("login")}?next={reverse("delete_product", args=[self.product.product_id])}')

    def test_product_list_view(self):
        response = self.client.get(reverse('products_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'roastery/products_list.html')
        self.assertContains(response, self.product.name)

    def test_product_detail_view(self):
        response = self.client.get(reverse('product_detail',
                                           args=[self.product.product_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_detail.html')
        self.assertContains(response, self.product.name)
