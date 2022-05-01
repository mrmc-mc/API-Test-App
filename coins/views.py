from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .permissions import TradePermission
from .serializers import TransactionSerializer, UserWalletSerializer


class TradeAPIView(CreateAPIView):
    """
    An endpoint for crreating a new transaction
    """

    permission_classes = [AllowAny]  # [IsAuthenticated, TradePermission]
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.jwt_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserWalletAPIView(ListAPIView):
    """
    An endpoint for retrieving a user's wallet
    """
    
    permission_classes = [AllowAny] #[IsAuthenticated]
    serializer_class = UserWalletSerializer
    
    def get_queryset(self):
        return self.request.user.uwallet.all()

    # def get_object(self):
    #     return self.request.user

    # def retrieve(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(self.get_object())
    #     return Response(serializer.data)