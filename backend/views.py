from rest_framework.views import APIView
from .models import ProductInfo, Product
from .serializers import ProductSerializer, ProductInfoSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from .models import Order, OrderItem, Contact
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

User = get_user_model()


class RegisterView(APIView):

    permission_classes = []

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "user exists"},
                status=400
            )


        try:
            User.objects.create_user(
                username=username,
                password=password
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=400
            )


        return Response({"status": "user created"})
#Товары
class ProductListView(APIView):

    def get(self, request):

        products = ProductInfo.objects.select_related(
            "product",
            "shop"
        )
        products = products.order_by("price")
        category = request.GET.get("category")
        shop = request.GET.get("shop")
        search = request.GET.get("search")

        if search:
            products = products.filter(
                product__name__icontains=search
            )
        if category:
            products = products.filter(product__category_id=category)

        if shop:
            products = products.filter(shop_id=shop)

        serializer = ProductInfoSerializer(products, many=True)

        return Response(serializer.data)

#Корзина
class BasketView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):

        order, _ = Order.objects.get_or_create(
            user=request.user,
            state="basket"
        )

        product = get_object_or_404(ProductInfo, id=request.data["product"])

        try:
            quantity = int(request.data.get("quantity", 1))
        except ValueError:
            return Response(
                {"error": "quantity must be integer"},
                status=400
            )

        item, created = OrderItem.objects.get_or_create(
            order=order,
            product_info=product,
        )
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()
        return Response({"status": "added"})

#Подтверждение

class ConfirmOrder(APIView):

    def post(self, request):

        order = Order.objects.get(
            user=request.user,
            state="basket"
        )

        contact = get_object_or_404(
            Contact,
            id=request.data["contact"],
            user=request.user)

        order.contact = contact
        order.state = "new"
        order.save()

        try:
            send_mail(
                "Order confirmation",
                "Ваш заказ принят",
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email]
            )
        except Exception:
            pass

        return Response({"status": "confirmed"})


class OrderConfirmView(APIView):

    def post(self, request):
        return Response({"status": "order confirmed"})