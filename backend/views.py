from rest_framework.views import APIView
from .models import ProductInfo, Product
from .serializers import ProductSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from .models import Order, OrderItem, Contact
from rest_framework.permissions import AllowAny

User = get_user_model()


class RegisterView(APIView):

    permission_classes = []

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "username and password required"},
                status=400
            )

        User.objects.create_user(
            username=username,
            password=password
        )

        return Response({"status": "user created"})
#Товары
class ProductListView(APIView):

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)

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


class OrderConfirmView(APIView):

    def post(self, request):
        return Response({"status": "order confirmed"})