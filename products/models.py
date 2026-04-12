from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True)


class Shop(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)


class ProductInfo(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name="products"
    )

    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_rrc = models.DecimalField(max_digits=10, decimal_places=2)

class Parameter(models.Model):
    name = models.CharField(max_length=100)


class ProductParameter(models.Model):

    product_info = models.ForeignKey(
        ProductInfo,
        on_delete=models.CASCADE,
        related_name="parameters"
    )

    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)