from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.prefetch_related('items__product').select_related('user')
    serializer_class = OrderSerializer
