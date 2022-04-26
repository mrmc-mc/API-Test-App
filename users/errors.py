from django.http import JsonResponse
from .utils import Jwt_handler
from rest_framework import status


MIDDLEWARE_ERROR = JsonResponse(data=None,
                            safe=False,
                            status=None,
                            content_type='application/json')


DATA_ERROR = JsonResponse(data={"jwt":Jwt_handler.encode(
                            {"message":"Unsupported Data"})},
                            safe=False,
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                            content_type='application/json')


OAUTH_ERROR = JsonResponse(data={"jwt":Jwt_handler.encode(
                            {"message":"otp required!"})},
                            safe=False,
                            status=status.HTTP_401_UNAUTHORIZED,
                            content_type='application/json')


# EMAIL_VERIFY_ERROR = JsonResponse(data=data,
#                                     safe=False,
#                                  status=status.HTTP_401_UNAUTHORIZED,
#                                  content_type='application/json')