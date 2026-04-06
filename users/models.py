from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    TYPE_CHOICES = (
        ("buyer", "Buyer"),
        ("supplier", "Supplier"),
    )

    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default="buyer"
    )

    email = models.EmailField(unique=True)