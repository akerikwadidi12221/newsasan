from django.core.management.base import BaseCommand
from tracking.models import RawClickEvent
import csv


class Command(BaseCommand):
    help = "Aggregate raw click events into a training CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            '--output', default='interactions_train.csv', help='CSV output path'
        )

    def handle(self, *args, **options):
        counts = {}
        for event in RawClickEvent.objects.all():
            if not event.user_id or not event.product_id:
                continue
            key = (event.user_id, event.product_id)
            counts[key] = counts.get(key, 0) + 1

        with open(options['output'], 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['user_id', 'product_id', 'count'])
            for (user_id, product_id), cnt in counts.items():
                writer.writerow([user_id, product_id, cnt])
        self.stdout.write(self.style.SUCCESS('CSV written'))
