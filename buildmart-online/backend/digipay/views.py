from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DigipayAccount
from .serializers import EligibilitySerializer, DigipayAccountSerializer


class EligibilityCheckView(APIView):
    """Mock eligibility check using a simple rule."""

    def post(self, request):
        serializer = EligibilitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        national_id = serializer.validated_data['national_id']
        # fake rule: even national IDs are eligible
        eligible = int(national_id[-1]) % 2 == 0
        return Response({'eligible': eligible})


class AccountInfoView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            account = DigipayAccount.objects.get(user=request.user)
        except DigipayAccount.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(DigipayAccountSerializer(account).data)
