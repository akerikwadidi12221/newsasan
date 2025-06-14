import csv
import os
from collections import defaultdict
from typing import List

class ItemBasedRecommender:
    def __init__(self, events_path: str):
        self.events_path = events_path
        self.product_users = defaultdict(set)
        self.similarity = {}

    def load_events(self):
        with open(self.events_path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.product_users[row["product_id"]].add(row["user_id"])

    def train(self):
        self.load_events()
        products = list(self.product_users.keys())
        for i, p1 in enumerate(products):
            for p2 in products[i+1:]:
                users1 = self.product_users[p1]
                users2 = self.product_users[p2]
                if not users1 or not users2:
                    score = 0.0
                else:
                    score = len(users1 & users2) / len(users1 | users2)
                if score > 0:
                    self.similarity.setdefault(p1, {})[p2] = score
                    self.similarity.setdefault(p2, {})[p1] = score

    def recommend(self, product_id: str, top_n: int = 3) -> List[str]:
        if product_id not in self.similarity:
            return []
        similar_items = sorted(self.similarity[product_id].items(), key=lambda x: x[1], reverse=True)
        return [item for item, _ in similar_items[:top_n]]

def main():
    base = os.path.dirname(__file__)
    rec = ItemBasedRecommender(os.path.join(base, 'sample_events.csv'))
    rec.train()
    for pid in ['p1', 'p2', 'p3', 'p4', 'p5']:
        recs = rec.recommend(pid)
        print(f'Recommendations for {pid}: {recs}')

if __name__ == '__main__':
    main()
