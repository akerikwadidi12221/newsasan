from rest_framework import serializers
from .models import DigipayAccount


class EligibilitySerializer(serializers.Serializer):
    national_id = serializers.CharField(max_length=20)


class DigipayAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigipayAccount
        fields = ['credit_limit', 'available_credit']
