import yaml

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from products.models import (
    Category,
    Product,
    ProductInfo,
    Shop,
    Parameter,
    ProductParameter,
)

User = get_user_model()


class Command(BaseCommand):
    help = "Импорт товаров из YAML файла"

    def add_arguments(self, parser):
        parser.add_argument("file", type=str)
        parser.add_argument("user_id", type=int)

    def handle(self, *args, **options):

        file_path = options["file"]
        user_id = options["user_id"]

        # Получаем пользователя
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR("User not found"))
            return

        #Проверка роли
        if user.type != "supplier":
            self.stdout.write(self.style.ERROR("User is not supplier"))
            return

        #Читаем YAML
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"File error: {e}"))
            return

        #Создаем / обновляем магазин
        shop, _ = Shop.objects.get_or_create(
            name=data["shop"],
            user=user
        )

        #Категории
        for category in data.get("categories", []):
            Category.objects.update_or_create(
                id=category["id"],
                defaults={"name": category["name"]}
            )

        #Товары
        for item in data.get("goods", []):


            product, _ = Product.objects.get_or_create(
                name=item["name"],
                category_id=item["category"]
            )


            product_info, _ = ProductInfo.objects.update_or_create(
                product=product,
                shop=shop,
                defaults={
                    "quantity": item["quantity"],
                    "price": item["price"],
                    "price_rrc": item["price_rrc"],
                }
            )


            for param in item.get("parameters", []):

                parameter, _ = Parameter.objects.get_or_create(
                    name=param["name"]
                )

                ProductParameter.objects.update_or_create(
                    product_info=product_info,
                    parameter=parameter,
                    defaults={
                        "value": param["value"]
                    }
                )

        self.stdout.write(self.style.SUCCESS("Import completed"))