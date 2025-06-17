from rest_framework import serializers
from .models import RawClickEvent


class RawClickEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawClickEvent
        fields = ["user", "product", "event_type", "metadata", "created_at"]
        read_only_fields = ["created_at"]
