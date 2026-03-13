from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .models import ProductInfo
from .serializers import ProductSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.core.mail import send_mail


from .models import (
    Order,
    OrderItem,
    Contact,
    ProductInfo,
    Shop,
    Category
)
User = get_user_model()

#Регистрация
class RegisterView(APIView):

    permission_classes = []

    def post(self, request):
        data = request.data
        user = User.objects.create_user(
            username=request.data["username"],
            email=request.data["email"],
            password=request.data["password"],
        )

        return Response({"status": "registered"})
#Товары
class ProductListView(ListAPIView):

    queryset = ProductInfo.objects.select_related("product", "shop")

    serializer_class = ProductSerializer

#Корзина
class BasketView(APIView):

    def post(self, request):

        order, _ = Order.objects.get_or_create(
            user=request.user,
            state="basket"
        )

        product = ProductInfo.objects.get(id=request.data["product"])

        OrderItem.objects.create(
            order=order,
            product_info=product,
            quantity=request.data["quantity"]
        )

        return Response({"status": "added"})

#Подтверждение

class ConfirmOrder(APIView):

    def post(self, request):

        order = Order.objects.get(
            user=request.user,
            state="basket"
        )

        contact = Contact.objects.get(id=request.data["contact"])

        order.contact = contact
        order.state = "new"
        order.save()

        send_mail(
            "Order confirmation",
            "Ваш заказ принят",
            None,
            [request.user.email]
        )

        return Response({"status": "confirmed"})


class OrderConfirmView:
    pass