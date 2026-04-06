from rest_framework.viewsets import ModelViewSet
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import ProductInfo, Order, OrderItem, Contact
from .serializers import (
    ProductInfoSerializer,
    OrderSerializer,
    ContactSerializer
)

User = get_user_model()


#товары
class ProductViewSet(ModelViewSet):

    queryset = ProductInfo.objects.select_related(
        "product",
        "shop"
    )
    serializer_class = ProductInfoSerializer

    def get_queryset(self):

        queryset = super().get_queryset()

        category = self.request.query_params.get("category")
        shop = self.request.query_params.get("shop")
        search = self.request.query_params.get("search")

        if category:
            queryset = queryset.filter(
                product__category_id=category
            )

        if shop:
            queryset = queryset.filter(
                shop_id=shop
            )

        if search:
            queryset = queryset.filter(
                product__name__icontains=search
            )

        return queryset


# корзина и заказы
class OrderViewSet(ModelViewSet):

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    # текущая корзина
    @action(detail=False, methods=["get"])
    def basket(self, request):

        order, _ = Order.objects.get_or_create(
            user=request.user,
            state="basket"
        )
        try:
            product_id = request.data.get("product")
            quantity = int(request.data.get("quantity", 1))
        except (TypeError, ValueError):
            return Response(
                {"error": "invalid input"},
                status=400
            )

        serializer = self.get_serializer(order)

        return Response(serializer.data)

    #добавить товар
    @action(detail=False, methods=["post"])
    def add(self, request):

        order, _ = Order.objects.get_or_create(
            user=request.user,
            state="basket"
        )

        product = get_object_or_404(
            ProductInfo,
            id=request.data.get("product")
        )

        try:
            quantity = int(request.data.get("quantity", 1))
        except ValueError:
            return Response(
                {"error": "quantity must be integer"},
                status=400
            )

        item, created = OrderItem.objects.get_or_create(
            order=order,
            product_info=product
        )

        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity

        item.save()

        return Response({"status": "added"})

    #удалить товар
    @action(detail=False, methods=["post"])
    def remove(self, request):

        item_id = request.data.get("item")

        OrderItem.objects.filter(
            id=item_id,
            order__user=request.user,
            order__state="basket"
        ).delete()

        return Response({"status": "deleted"})

    # подтвердить заказ
    @action(detail=False, methods=["post"])
    def confirm(self, request):

        order = get_object_or_404(
            Order,
            user=request.user,
            state="basket"
        )

        if not order.items.exists():
            return Response(
                {"error": "basket empty"},
                status=400
            )

        contact = get_object_or_404(
            Contact,
            id=request.data.get("contact"),
            user=request.user
        )

        order.contact = contact
        order.state = "new"
        order.save()

        return Response({"status": "confirmed"})

    # изменить статус заказа
    @action(detail=True, methods=["post"])
    def set_status(self, request, pk=None):

        order = self.get_object()

        order.state = request.data.get("state")
        order.save()

        return Response({"status": "updated"})

    def export_products(request):

        data = list(ProductInfo.objects.values())

        return JsonResponse(data, safe=False)

# КОНТАКТЫ
class ContactViewSet(ModelViewSet):

    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    queryset = Contact.objects.all()
    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


