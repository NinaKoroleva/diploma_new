from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)


class Shop(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.BooleanField(default=True)


class Category(models.Model):
    name = models.CharField(max_length=50)


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    price_rrc = models.PositiveIntegerField()


class Parameter(models.Model):
    name = models.CharField(max_length=40)


class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    value = models.CharField(max_length=40)


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=15)


class Order(models.Model):

    STATUS = (
        ("basket", "Basket"),
        ("new", "New"),
        ("confirmed", "Confirmed"),
        ("shipped", "Shipped"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True)
    state = models.CharField(max_length=20, choices=STATUS)
    dt = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()