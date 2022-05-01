from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .permissions import TradePermission
from .serializers import TransactionSerializer


class TradeAPIView(CreateAPIView):
    '''
        An endpoint for crreating a new transaction
    '''
    permission_classes = [AllowAny]  # [IsAuthenticated, TradePermission]
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.jwt_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
