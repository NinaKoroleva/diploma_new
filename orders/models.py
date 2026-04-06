from django.db import models
from users.models import User
from products.models import ProductInfo


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=15)
    phone = models.CharField(max_length=20)


class Order(models.Model):

    STATUS = (
        ("basket", "Basket"),
        ("new", "New"),
        ("confirmed", "Confirmed"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True)
    state = models.CharField(max_length=20, choices=STATUS, default="basket")


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )

    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ("order", "product_info")