from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, PersonalInfoSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny
from .utils import Jwt_handler
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.core.files.base import ContentFile
from django.utils.timezone import now
from django.contrib import auth
from django.conf import settings
import datetime
from django.core.cache import cache


User = get_user_model()


class RegisterAPIView(APIView):
    # Allow any user (authenticated or not) to access this url 
    permission_classes = (AllowAny,)
 
    def post(self, request):
        try:
            reg_data = request.data
            img_base64 = request.data.get("image_file")

            img_FileCode = ContentFile(img_base64,
                                f"{request.data['first_name']}_{request.data['last_name']}-{now()}.txt")
            reg_data["image_file"] = img_FileCode
            user_serializer = UserSerializer(data=reg_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
            print(type(user))

            info_serializer = PersonalInfoSerializer(instance=user, data=reg_data)
            if info_serializer.is_valid(raise_exception=True):
                info_serializer.save()


            status_code = status.HTTP_201_CREATED
            result= {}
            result['info'] = info_serializer.data
            result['user'] = user_serializer.data

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            result = {"message":str(e)}
        
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

            auth.login(request, user)

            data = {
                'message': "success"
            }
            status_code = status.HTTP_200_OK

        except:
            data = {
                'message': "somthing wrong"
            }
            status_code = status.HTTP_400_BAD_REQUEST

        response = Jwt_handler.encode(data)
        return Response(response, status=status_code)


class OtpRegVerificationAPIView(APIView):

    def post(self, request):

            u_otp = request.POST['otp']
            otp = cache.get(f"{user.id}_reg_otp")
            cache.delete(f"{user.id}_reg_otp")
            if int(u_otp) == otp:
                user = authenticate(request,username=username,password=password)
                if user is not None:
                    login(request,user)
                    request.session.delete('login_otp')
                    messages.success(request,'login successfully')
                    return redirect('/')
            else:
                messages.error(request,'Wrong OTP')
                
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