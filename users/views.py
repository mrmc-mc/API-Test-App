from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny
from .utils import verify_captcha, Jwt_handler
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.core.files.base import ContentFile
from django.utils.timezone import now
from django.contrib import auth
from django.conf import settings
import datetime
import jwt

User = get_user_model()


class RegisterAPIView(APIView):
    # Allow any user (authenticated or not) to access this url 
    permission_classes = (AllowAny,)
 
    def post(self, request):
        user = request.data
        img_base64 = request.data.get("image_file")
        #google = request.data["google-code"]
        #g_response = request.data.get('g-recaptcha-response')
        img_FileCode = ContentFile(img_base64,
                            f"{request.data['first_name']}_{request.data['last_name']}-{now()}.txt")

        user["image_file"] = img_FileCode
        #if verify_captcha(g_response):
        if True:
                serializer = UserSerializer(data=user)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                status_code = status.HTTP_201_CREATED
        else:
                status_code = status.HTTP_400_BAD_REQUEST

        result = serializer.data or "Captcha does not correct!"
        return Response(result, status=status_code)


class LoginAPIView(APIView):
    def post(self, request):

        try:
            payload = Jwt_handler.decode(token=request.data['jwt'])
            email = payload['email']
            password = payload['password']

            user = User.objects.filter(email=email).first()

            if user is None:
                raise AuthenticationFailed('User not found!')

            if not user.check_password(password):
                raise AuthenticationFailed('Incorrect password!')


            data = {
                'message': "success"
            }
        except:
            data = {
                'message': "somthing wrong"
            }

        return Response(data)


class UserAPIView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = 1
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutAPIView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        # auth.logout(request)
        response.data = {
            'message': 'success'
        }
        return response