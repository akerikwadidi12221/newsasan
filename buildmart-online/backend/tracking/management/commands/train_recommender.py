from django.core.management.base import BaseCommand
import os
import json
from collections import defaultdict


class Command(BaseCommand):
    help = "Train a simple item-based recommender from interactions CSV"

    def add_arguments(self, parser):
        parser.add_argument('csv', help='interactions csv path')
        parser.add_argument('--output', default='recommendations.json')

    def handle(self, csv, *args, **options):
        product_users = defaultdict(set)
        with open(csv) as f:
            next(f)
            for line in f:
                user_id, product_id, count = line.strip().split(',')
                product_users[product_id].add(user_id)

        similarity = {}
        products = list(product_users.keys())
        for i, p1 in enumerate(products):
            for p2 in products[i+1:]:
                users1 = product_users[p1]
                users2 = product_users[p2]
                if not users1 or not users2:
                    score = 0.0
                else:
                    score = len(users1 & users2) / len(users1 | users2)
                if score > 0:
                    similarity.setdefault(p1, {})[p2] = score
                    similarity.setdefault(p2, {})[p1] = score

        with open(options['output'], 'w') as f:
            json.dump(similarity, f)
        self.stdout.write(self.style.SUCCESS('Model saved'))
