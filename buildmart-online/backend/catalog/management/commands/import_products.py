import csv
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from catalog.models import Product, ProductImage, Category, Brand
from django.db import transaction

class Command(BaseCommand):
    help = "Import products and their images from a CSV file."

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Path to the CSV file")

    @transaction.atomic  # اگر خطا شد، همه چیز برمی‌گردد
    def handle(self, *args, **options):
        csv_path = Path(options["csv_path"])
        if not csv_path.exists():
            raise CommandError(f"File {csv_path} not found!")

        with csv_path.open(newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # 1) دسته و برند را پیدا کن یا بساز
                category_obj, _ = Category.objects.get_or_create(name=row["category"])
                brand_obj, _    = Brand.objects.get_or_create(name=row["brand"])

                # 2) محصول را بساز
                product = Product.objects.create(
                    name=row["name"],
                    description=row["description"],
                    category=category_obj,
                    brand=brand_obj,
                    price=row["price"],
                    stock_quantity=row["stock_quantity"],
                )

                # 3) عکس‌هایش را بساز (اولی primary)
                for idx in range(1, 4):  # image_url1 تا image_url3
                    url_key = f"image_url{idx}"
                    url = row.get(url_key)
                    if url:  # خالی نباشد
                        ProductImage.objects.create(
                            product=product,
                            image_url=url.strip(),
                            is_primary=(idx == 1),
                            display_order=idx,
                        )

                self.stdout.write(self.style.SUCCESS(f"Imported {product.name}"))

        self.stdout.write(self.style.SUCCESS("All done!"))