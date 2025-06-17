from fastapi import FastAPI, HTTPException
import json
import os

app = FastAPI()

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'recommendations.json')
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH) as f:
        SIMILARITY = json.load(f)
else:
    SIMILARITY = {}

POPULAR_PRODUCTS = ['1', '2', '3']

@app.get('/api/recommendations/')
def recommendations(user_id: str | None = None, product_id: str | None = None):
    if user_id and product_id:
        sims = SIMILARITY.get(product_id, {})
        sorted_items = sorted(sims.items(), key=lambda x: x[1], reverse=True)
        recs = [pid for pid, _ in sorted_items[:5]]
    else:
        recs = POPULAR_PRODUCTS
    return {'recommendations': recs}
