from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny
from .utils import verify_captcha
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.core.files.base import ContentFile
from django.utils.timezone import now

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
                serializer = RegisterSerializer(data=user)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                status_code = status.HTTP_201_CREATED
        else:
                status_code = status.HTTP_400_BAD_REQUEST

        result = serializer.data or "Captcha does not correct!"
        return Response(result, status=status_code)


class LoginAPIView(APIView):

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')


        token = RefreshToken.for_user(user)

        response = Response()

        response.set_cookie(key='jwt', value=str(token.access_token), httponly=True)
        response.data = {
            'jwt': str(token.access_token)
        }
        return response


class LogoutAPIView(APIView):

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response