from django.db import models
from django.conf import settings
from catalog.models import Product


class RawClickEvent(models.Model):
    """Store raw clickstream events for training the recommender."""

    EVENT_TYPES = [
        ("product_view", "Product View"),
        ("add_to_cart", "Add to Cart"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    metadata = models.JSONField(blank=True, default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["event_type", "created_at"])]

    def __str__(self) -> str:
        return f"{self.user} {self.event_type} {self.product}"  # pragma: no cover
