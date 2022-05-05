from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import JWTBaseSearchFilter
from .paginators import UserListSetPagination

from .serializers import (
    ChangePasswordSerializer,
    PersonalInfoSerializer,
    UserListSerializer,
    UserMediaSerializer,
    UserSerializer,
)
from .utils import Email, Oauth_handler

# from  rest_framework.generics import ListCreateAPIView


User = get_user_model()


class RegisterAPIView(APIView):  # Can use rest_framework.generics.ListCreateAPIView
    """
    An endpoint for register user.
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            reg_data = request.jwt_data
            user_serializer = UserSerializer(data=reg_data)
            if user_serializer.is_valid(raise_exception=True):
                user = user_serializer.save()
                group = Group.objects.get(name="registered_group")
                user.groups.add(group)

            reg_data["user"] = user.pk
            info_serializer = PersonalInfoSerializer(data=reg_data)
            info_serializer.is_valid(raise_exception=True)
            info_serializer.save()

            media_serializer = UserMediaSerializer(data=reg_data)
            media_serializer.is_valid(raise_exception=True)
            media_serializer.save()

            status_code = status.HTTP_201_CREATED
            result = {}
            result["info"] = info_serializer.data
            result["user"] = user_serializer.data
            result["media"] = media_serializer.data

        except Exception as e:
            if "user" in locals():
                user.delete()

            status_code = status.HTTP_400_BAD_REQUEST
            result = {"message": str(e)}

        return Response(result, status=status_code)


class LoginAPIView(APIView):
    """
    An endpoint for login.
    """

    def post(self, request):

        data = {}

        try:
            payload = request.jwt_data
            email = payload["email"]
            password = payload["password"]

            user = User.objects.filter(email=email).first()

            if user is None:
                raise AuthenticationFailed(
                    detail="User not found!", code=status.HTTP_404_NOT_FOUND
                )

            if not user.check_password(password):
                raise AuthenticationFailed(
                    detail="Incorrect password!", code=status.HTTP_400_BAD_REQUEST
                )

            auth.login(request, user)

            if user.uauth.is_enabled:
                data["required"] = "otp"
                request.session["otp"] = "unverified"

            data["message"] = "success"

            status_code = status.HTTP_200_OK

        except Exception as e:
            data = {"message": "somthing wrong"}
            status_code = status.HTTP_400_BAD_REQUEST

        response = data
        return Response(response, status=status_code)


class OtpRegVerificationAPIView(APIView):
    """
    An endpoint for very email otp code[register].
    """

    permission_classes = (IsAuthenticated,)
    # renderer_classes = []

    def post(self, request):

        if not request.user.is_email_verified:
            try:
                if Email.VerifyRegisterationOTP(request=request):
                    user = request.user
                    user.is_email_verified = True
                    user.save()
                    data = {"message": "Email successfully verified"}
                    status_code = status.HTTP_200_OK

                else:
                    data = {"message": "Email not verified"}
                    status_code = status.HTTP_400_BAD_REQUEST

            except Exception as e:
                data = {"message": "somthing wrong"}
                status_code = status.HTTP_417_EXPECTATION_FAILED

        else:
            data = {"message": "Email verified"}
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(data=data, status=status_code)


class LogoutAPIView(APIView):
    """
    An endpoint for logout user.
    """

    def post(self, request):
        response = Response()
        auth.logout(request)
        response.data = {"message": "success"}
        response.status = status.HTTP_200_OK
        return response


class ChangePasswordAPIView(UpdateAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.user.set_password(serializer.data.get("new_password"))
            self.user.save()
            data = {
                "status": "success",
                "message": "Password updated successfully",
            }

            return Response(data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OauthAPIView(APIView):
    """
    An endpoint for verify otp code after login.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        print(request.jwt_data)
        try:
            # if request.session['otp'] == "unverified":
            if Oauth_handler.verify_otp(request.user, request.jwt_data["otp"]):

                request.session["otp"] = "verified"
                data = {"message": "otp successfully verified"}
                status_code = status.HTTP_200_OK

            else:
                data = {"message": "otp is incorrect!"}
                status_code = status.HTTP_401_UNAUTHORIZED

        # data = {
        #         'message': "somthing wrong"
        #         }
        # status_code = status.HTTP_417_EXPECTATION_FAILED

        except Exception as e:
            data = {"message": "otp error!"}
            status_code = status.HTTP_417_EXPECTATION_FAILED
            print(e)

        response = data
        return Response(response, status=status_code)


class UserListAPIView(ListAPIView):
    """
    An endpoint for listing all users.
    """
    
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    # pagination_class = UserListSetPagination



    def get_queryset(self):
        return User.objects.all()


    # def post(self, request, *args, **kwargs):
    #     print(request.jwt_data["filter"])
    #     try:
    #         queryset = self.get_queryset()
    #         filter_params = None
            
    #         if 'filter' in request.jwt_data:
    #             filter_params = request.jwt_data["filter"]
    #             print(filter_params)
    #         if filter_params:
    #             queryfilter = self.filterset_class(filter_params, queryset=queryset)
    #             queryset = queryfilter.qs

    #         serializer = self.serializer_class(queryset, many=True)
    #         data = serializer.data
    #         status_code = status.HTTP_200_OK
    #     except KeyError:
    #         data = {"message": "Invalid data!"}
    #         status_code = status.HTTP_400_BAD_REQUEST
            
    #     return Response(data=data, status=status_code)
    
    def post(self, request, *args, **kwargs):
        self.filter_backends = [JWTBaseSearchFilter]
        self.search_fields = [
            "phone",
            "email",
            "uinfo__first_name",
            "uinfo__last_name",
            "uinfo__national_code",
            "can_trade",
            ]
        params = request.jwt_data.get('search', '')
        print(params)
        return self.list(request, *args, **kwargs)