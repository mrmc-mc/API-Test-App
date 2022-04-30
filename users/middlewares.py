from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import reverse
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError
from rest_framework import status
from rest_framework.utils import json

from .errors import OAUTH_ERROR
from .utils import Email, Jwt_handler

User = get_user_model()


EMAIL_UNVERIFIED_EXCLUDE_PATH = [
    reverse("users:email-verify"),
    reverse("users:otp-verify"),
    "/admin/",
]

OAUTH_EXCLUDE_PATH = [
    reverse("users:otp-verify"),
]


class ActiveEmailMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        if (
            request.user.is_authenticated
            and not request.user.is_email_verified
            and request.path not in EMAIL_UNVERIFIED_EXCLUDE_PATH
        ):

            data = {"message": "Email is not verified"}
            data["OTP"] = "Already sended to your email"

            if not cache.get(f"{request.user.id}_reg_otp"):
                Email.SendRegisterationOTP(instance=request.user)
                data["OTP"] = "sent"

            return JsonResponse(
                data={"jwt": Jwt_handler.encode(data)},
                safe=False,
                status=status.HTTP_401_UNAUTHORIZED,
                content_type="application/json",
            )

        else:
            response = self.get_response(request)

            # Code to be executed for each request/response after
            # the view is called.

            return response


class OauthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)
        _path = request.path

        if request.user.is_authenticated and request.user.uauth.is_enabled:

            if "otp" in request.session and str(request.session["otp"]) == "verified":

                if _path in OAUTH_EXCLUDE_PATH:
                    return JsonResponse(
                        data={
                            "jwt": Jwt_handler.encode({"message": "somthing wrong!"})
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                else:
                    return response

            elif _path not in OAUTH_EXCLUDE_PATH:
                return OAUTH_ERROR

            else:
                print("!" * 90)
                return response

        else:
            return response


class UserActiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        if request.user.is_authenticated and not request.user.uauth.can_trade:

                    return JsonResponse(
                        data={
                            "jwt": Jwt_handler.encode({"message": "your account is limited!"})
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )
        else:
            return response


class DataToJwtMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        if hasattr(response, "data"):
            _data = json.dumps(
                {"jwt": (Jwt_handler.encode(response.data))},
                indent=8,
                sort_keys=True,
                default=DjangoJSONEncoder,
            )
            response.data = _data
            response.content = [_data]

        return response


class JwtToDataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.method != "GET":
            if hasattr(request, "body"):
                if b"jwt" in request.body:
                    try:
                        __token = Jwt_handler.decode(json.loads(request.body)["jwt"])
                        request.jwt_data = __token

                    except InvalidSignatureError or ExpiredSignatureError:
                        
                        return JsonResponse(
                            data={
                                "jwt": Jwt_handler.encode(
                                    {"error": "Signature verification failed!"}
                                )
                            },
                            status=status.HTTP_401_UNAUTHORIZED,
                        )

        response = self.get_response(request)

        return response
