from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from backend.models import Product, ProductInfo, Product, Shop

User = get_user_model()

#тест корзины
class BasketTest(TestCase):

    def setUp(self):

        self.client = APIClient()

        self.user = User.objects.create_user(
            username="test",
            password="123"
        )

        self.client.force_authenticate(self.user)

        shop = Shop.objects.create(name="Shop1", user=self.user)

        product = Product.objects.create(name="Phone")

        self.product_info = ProductInfo.objects.create(
            product=product,
            shop=shop,
            quantity=10,
            price=100
        )

    def test_add_to_basket(self):

        response = self.client.post(
            "/api/basket/",
            {
                "product": self.product_info.id,
                "quantity": 1
            }
        )

        self.assertEqual(response.status_code, 200)
#тест регистрации
class RegisterTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):

        response = self.client.post(
            "/api/register/",
            {
                "username": "testuser",
                "password": "123456"
            }
        )

        self.assertEqual(response.status_code, 200)
#тест список товаров
class ProductTest(TestCase):

    def setUp(self):

        self.client = APIClient()

        Product.objects.create(
            name="iPhone",
            description="phone"
        )

    def test_product_list(self):

        response = self.client.get("/api/products/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)