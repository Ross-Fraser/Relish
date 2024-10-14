from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import User, Permission
from roastery.models import Product, Category, CoffeeOrigin, CoffeeGrind, CoffeeSize
from .models import BagItem

class BagViewsTestCase(TestCase):
    
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
        
        # Create BagItem
        self.bag_item = BagItem.objects.create(user=self.user, product=self.product, quantity=1)
    
    def test_bag_detail_view(self):
        """Test bag detail view shows bag items and total price"""
        response = self.client.get(reverse('bag:bag_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bag_detail.html')
        self.assertContains(response, 'Test Product')
        self.assertContains(response, '10.00') # Price of the product

    def test_add_to_bag_view(self):
        """Test adding a product to the bag"""
        product_id = self.product.id
        response = self.client.post(reverse('bag:add_to_bag', args=[product_id]))
        self.assertRedirects(response, reverse('bag:bag_detail'))
        bag_item = BagItem.objects.get(user=self.user, product=self.product)
        self.assertEqual(bag_item.quantity, 2)  # Since the product was already in the bag
    
    def test_update_bag_item_view(self):
        """Test updating the quantity of a bag item"""
        bag_item_id = self.bag_item.id
        response = self.client.post(reverse('bag:update_bag_item', args=[bag_item_id]), {'quantity': 3})
        self.assertRedirects(response, reverse('bag:bag_detail'))
        updated_item = BagItem.objects.get(id=bag_item_id)
        self.assertEqual(updated_item.quantity, 3)

    def test_remove_from_bag_view(self):
        """Test removing a product from the bag"""
        bag_item_id = self.bag_item.id
        response = self.client.post(reverse('bag:remove_from_bag', args=[bag_item_id]))
        self.assertRedirects(response, reverse('bag:bag_detail'))
        with self.assertRaises(BagItem.DoesNotExist):
            BagItem.objects.get(id=bag_item_id)
