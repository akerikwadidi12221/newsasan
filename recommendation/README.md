# Recommendation Example

This folder contains a simple item-based collaborative filtering example.

`sample_events.csv` holds sample click events for a few products. The
`recommender.py` script computes product-to-product similarity using
Jaccard similarity of users who viewed each item and prints some example
recommendations.

Run it with:

```bash
python recommendation/recommender.py
```
