from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import TyreModel, TyreVariant, Category, Favourite
from decimal import Decimal

User = get_user_model()

class TyreModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Тестовая категория',
            slug='test-category',
            type='tyre'
        )
        self.tyre_model = TyreModel.objects.create(
            name='Test Tyre',
            brand='Test Brand',
            description='Test Description'
        )
        self.tyre_variant = TyreVariant.objects.create(
            model=self.tyre_model,
            width=205,
            profile=55,
            radius=16,
            season='summer',
            speed_index='H',
            price=Decimal('10000.00'),
            stock=10
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = Client()

    def test_tyre_model_creation(self):
        self.assertEqual(self.tyre_model.name, 'Test Tyre')
        self.assertEqual(self.tyre_model.brand, 'Test Brand')
        self.assertEqual(str(self.tyre_model), 'Test Brand Test Tyre')

    def test_tyre_variant_creation(self):
        self.assertEqual(self.tyre_variant.width, 205)
        self.assertEqual(self.tyre_variant.profile, 55)
        self.assertEqual(self.tyre_variant.radius, 16)
        self.assertEqual(self.tyre_variant.price, Decimal('10000.00'))
        self.assertTrue(self.tyre_variant.is_in_stock())
        self.assertTrue(self.tyre_variant.can_order(5))
        self.assertFalse(self.tyre_variant.can_order(15))

    def test_tyre_variant_validation(self):
        # Test invalid width
        with self.assertRaises(Exception):
            TyreVariant.objects.create(
                model=self.tyre_model,
                width=100,  # Too small
                profile=55,
                radius=16,
                season='summer',
                speed_index='H',
                price=Decimal('10000.00'),
                stock=10
            )

        # Test invalid price
        with self.assertRaises(Exception):
            TyreVariant.objects.create(
                model=self.tyre_model,
                width=205,
                profile=55,
                radius=16,
                season='summer',
                speed_index='H',
                price=Decimal('-1000.00'),  # Negative price
                stock=10
            )

    def test_favourite_functionality(self):
        # Test adding to favourites
        favourite = Favourite.objects.create(
            user=self.user,
            variant=self.tyre_variant
        )
        self.assertEqual(favourite.user, self.user)
        self.assertEqual(favourite.variant, self.tyre_variant)

        # Test duplicate favourite
        with self.assertRaises(Exception):
            Favourite.objects.create(
                user=self.user,
                variant=self.tyre_variant
            )

    def test_category_functionality(self):
        # Test category creation
        self.assertEqual(self.category.name, 'Тестовая категория')
        self.assertEqual(self.category.slug, 'test-category')
        self.assertEqual(self.category.type, 'tyre')

        # Test category URL
        self.assertEqual(self.category.get_absolute_url(), '/catalog/test-category/')

        # Test subcategory
        subcategory = Category.objects.create(
            name='Subcategory',
            slug='subcategory',
            type='tyre',
            parent=self.category
        )
        self.assertEqual(subcategory.parent, self.category)
        self.assertEqual(list(self.category.children.all()), [subcategory])

class CartTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        self.tyre_model = TyreModel.objects.create(
            name='Test Tyre',
            brand='Test Brand',
            description='Test Description'
        )
        self.tyre_variant = TyreVariant.objects.create(
            model=self.tyre_model,
            width=205,
            profile=55,
            radius=16,
            season='summer',
            speed_index='H',
            price=Decimal('10000.00'),
            stock=10
        )

    def test_add_to_cart(self):
        response = self.client.post(
            reverse('add_to_cart'),
            {
                'variant_id': self.tyre_variant.id,
                'quantity': 2
            }
        )
        self.assertEqual(response.status_code, 200)
        
        # Check cart in session
        session = self.client.session
        self.assertIn('cart', session)
        self.assertEqual(session['cart'][str(self.tyre_variant.id)], 2)

    def test_remove_from_cart(self):
        # First add item to cart
        self.client.post(
            reverse('add_to_cart'),
            {
                'variant_id': self.tyre_variant.id,
                'quantity': 2
            }
        )
        
        # Then remove it
        response = self.client.post(
            reverse('remove_from_cart'),
            {
                'variant_id': self.tyre_variant.id
            }
        )
        self.assertEqual(response.status_code, 200)
        
        # Check cart is empty
        session = self.client.session
        self.assertNotIn(str(self.tyre_variant.id), session.get('cart', {}))

    def test_cart_quantity_validation(self):
        # Test adding more than available
        response = self.client.post(
            reverse('add_to_cart'),
            {
                'variant_id': self.tyre_variant.id,
                'quantity': 15  # More than stock
            }
        )
        self.assertEqual(response.status_code, 400)
        
        # Test adding negative quantity
        response = self.client.post(
            reverse('add_to_cart'),
            {
                'variant_id': self.tyre_variant.id,
                'quantity': -1
            }
        )
        self.assertEqual(response.status_code, 400)

class OrderTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        self.tyre_model = TyreModel.objects.create(
            name='Test Tyre',
            brand='Test Brand',
            description='Test Description'
        )
        self.tyre_variant = TyreVariant.objects.create(
            model=self.tyre_model,
            width=205,
            profile=55,
            radius=16,
            season='summer',
            speed_index='H',
            price=Decimal('10000.00'),
            stock=10
        )
        
        # Add item to cart
        self.client.post(
            reverse('add_to_cart'),
            {
                'variant_id': self.tyre_variant.id,
                'quantity': 2
            }
        )

    def test_create_order(self):
        response = self.client.post(
            reverse('create_order'),
            {
                'first_name': 'Test',
                'last_name': 'User',
                'email': 'test@example.com',
                'phone': '+79001234567',
                'address': 'Test Address'
            }
        )
        self.assertEqual(response.status_code, 200)
        
        # Check stock was updated
        self.tyre_variant.refresh_from_db()
        self.assertEqual(self.tyre_variant.stock, 8)
        
        # Check cart was cleared
        session = self.client.session
        self.assertNotIn('cart', session)

    def test_create_order_validation(self):
        # Test without required fields
        response = self.client.post(
            reverse('create_order'),
            {
                'first_name': 'Test',
                'last_name': 'User'
                # Missing required fields
            }
        )
        self.assertEqual(response.status_code, 400)
        
        # Test with invalid phone
        response = self.client.post(
            reverse('create_order'),
            {
                'first_name': 'Test',
                'last_name': 'User',
                'email': 'test@example.com',
                'phone': 'invalid',
                'address': 'Test Address'
            }
        )
        self.assertEqual(response.status_code, 400)
