from rest_framework import viewsets
from .models import Cart
from .serializers import CartSerializer


class CartViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cart.objects.prefetch_related('items__product').select_related('user')
    serializer_class = CartSerializer
