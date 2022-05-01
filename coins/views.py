from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

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


class UserWalletAPIView(ReadOnlyModelViewSet):
    """
    An endpoint for retrieving a user's wallet
    """

    permission_classes = [AllowAny]  # [IsAuthenticated]
    serializer_class = UserWalletSerializer

    def get_queryset(self):
        return self.request.user.uwallet.all()

    def get_object(self):
        return self.request.user.uwallet.get(
            coin__symbol=(self.request.jwt_data["symbol"]).upper()
        )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            data = serializer.data
            code_status = status.HTTP_200_OK
        except ObjectDoesNotExist:
            data = {"message": "incorrect symbol!"}
            code_status = status.HTTP_404_NOT_FOUND

        return Response(data=data, status=code_status)
