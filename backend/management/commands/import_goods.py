import yaml
from django.core.management.base import BaseCommand
from backend.models import *


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("file")

    def handle(self, *args, **options):

        with open(options["file"]) as f:
            data = yaml.safe_load(f)

        shop = Shop.objects.create(name=data["shop"], user_id=1)

        for cat in data["categories"]:
            Category.objects.get_or_create(
                id=cat["id"],
                name=cat["name"]
            )

        for item in data["goods"]:

            category = Category.objects.get(id=item["category"])

            product = Product.objects.create(
                name=item["name"],
                category=category
            )

            product_info = ProductInfo.objects.create(
                product=product,
                shop=shop,
                price=item["price"],
                price_rrc=item["price"],
                quantity=item["quantity"]
            )