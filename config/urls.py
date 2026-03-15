from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("API is running")

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('', include('backend.urls')),
]


# #from django.contrib import admin
# #from django.urls import path, include
#
# #from backend.views import (
#     RegisterView,
#     ProductListView,
#     BasketView,
#     OrderConfirmView
# )
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('backend.urls')),
#
#     path('user/register', RegisterView.as_view()),
#     path('products', ProductListView.as_view()),
#     path('basket', BasketView.as_view()),
#     path('order/confirm', OrderConfirmView.as_view()),
# ]
