from django.http import JsonResponse
from .models import ProductInfo
from rest_framework.response import Response


def export_products(request):

    data = list(ProductInfo.objects.values())
    try:
        quantity = int(request.data.get("quantity"))
    except:
        return Response({"error": "invalid quantity"}, status=400)
    return JsonResponse(data, safe=False)
