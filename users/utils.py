# Tools
from django.conf import settings
import jwt


def user_upload_dir(instance , filename):
    """  set upload directroy by user id and change file name   """

    return f'user_{instance.national_code}/{filename}'



def verify_captcha(response):
    
    from django.conf import settings
    import requests
    
    ''' reCAPTCHA validation '''
    recaptcha_response = response
    data = {
    'secret': settings.RECAPTCHA_PRIVATE_KEY,
    'response': recaptcha_response
    }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = r.json()

    print(result)

    ''' if reCAPTCHA returns True '''
    if result['success']:
        return True
    else:
        return False


class Jwt_handler:
    """  Module for Encode/Decode JWT   """


    @staticmethod
    def encode(payload):
        token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm='HS256')
        return token


    @staticmethod
    def decode(token):
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        return payload