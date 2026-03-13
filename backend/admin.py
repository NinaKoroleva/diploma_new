from django.contrib import admin
from .models import Product, Order, OrderItem, Contact, User

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Contact)
admin.site.register(User)