from django.core.management.base import BaseCommand
from catalog.models import Category

class Command(BaseCommand):
    help = "Create the main brand categories if they don't already exist"

    def handle(self, *args, **options):
        categories = [
            'لوله واتصالات پنج لایه نیوپایپ',
            'لوله و اتصالات تک لایه آذین',
            'لوله و اتصالات فاضلابی مولتی پایپ',
            'محصولات پلی اتیلن آبیاری دینا پلیمر',
        ]
        for order, name in enumerate(categories, start=1):
            obj, created = Category.objects.get_or_create(
                name=name,
                defaults={'display_order': order}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created {obj.name}"))
            else:
                self.stdout.write(f"{obj.name} already exists")
