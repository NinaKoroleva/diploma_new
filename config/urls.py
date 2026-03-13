from django.contrib import admin
from django.urls import path

from backend.views import (
    RegisterView,
    ProductListView,
    BasketView,
    OrderConfirmView
)

urlpatterns = [
    path('admin/', admin.site.urls),


    path('user/register', RegisterView.as_view()),
    path('products', ProductListView.as_view()),
    path('basket', BasketView.as_view()),
    path('order/confirm', OrderConfirmView.as_view()),
]
