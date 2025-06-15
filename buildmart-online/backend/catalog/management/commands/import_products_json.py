import json
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from catalog.models import Product, Category

class Command(BaseCommand):
    help = "Import products from a JSON file"

    def add_arguments(self, parser):
        parser.add_argument(
            'json_path', type=str, nargs='?', default='database/space/got.json',
            help='Path to the JSON file with product info'
        )
        parser.add_argument(
            '--category', type=int, default=1,
            help='ID of the category to assign to imported products'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        json_path = Path(options['json_path'])
        if not json_path.exists():
            raise CommandError(f'File {json_path} not found!')

        try:
            category = Category.objects.get(pk=options['category'])
        except Category.DoesNotExist:
            raise CommandError('Specified category does not exist')

        with json_path.open(encoding='utf-8') as f:
            products = json.load(f)

        for item in products:
            code = item.get('code')
            name = item.get('name', '')
            if not code or not name:
                self.stderr.write('Skipping invalid item')
                continue
            obj, created = Product.objects.update_or_create(
                code=code,
                defaults={
                    'name': name,
                    'category': category,
                }
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(self.style.SUCCESS(f'{action} {obj.code}'))

        self.stdout.write(self.style.SUCCESS('Import finished'))
