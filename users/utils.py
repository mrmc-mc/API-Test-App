# Tools
import threading
from random import randrange

import jwt
import pyotp
from django.conf import settings
from django.contrib.sites.models import Site
# from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.core.mail import send_mail
from django.template.loader import render_to_string


def user_upload_dir(instance, filename):
    """set upload directroy by user id and change file name"""

    return f"user_{instance.national_code}/{filename}"


class Jwt_handler:
    """Module for Encode/Decode JWT"""

    @staticmethod
    def encode(payload):
        token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm="HS256")
        return token

    @staticmethod
    def decode(token):
        try:
            payload = jwt.decode(
                jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"]
            )
            return payload
        # except jwt.exceptions.InvalidSignatureError as e:
        except Exception as e:
            print(f"Erorr: {e}")


class EmailThread(threading.Thread):
    def __init__(self, subject, body, sender, email):
        self.subject = subject
        self.body = body
        self.message = body
        self.sender = sender
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        """send an email"""

        try:

            send_mail(
                subject=self.subject,
                message=None,
                html_message=self.body,
                from_email=self.sender,
                recipient_list=self.email,
                fail_silently=False,
            )

            return True

        except Exception as e:
            return False


class Email:
    @staticmethod
    def SendRegisterationOTP(instance):

        try:
            user = instance
            otp = randrange(100000, 999999)
            cache.set(f"{user.id}_reg_otp", otp, timeout=3600 * 24 * 7)
            subject = "Verification Code"
            payload = {"otp": otp}
            email_template_name = "users/auth_email_verify.html"
            index = {
                "email": user.email,
                "text": f"TOPKENZ.COM: Your OTP code is: {otp}",
                "jwt": Jwt_handler.encode(payload),
            }
            body = render_to_string(email_template_name, index)

            EmailThread(
                subject=subject,
                body=body,
                sender=settings.DEFAULT_FROM_EMAIL,
                email=[
                    user.email,
                ],
            ).start()

        # except BadHeaderError:
        #     pass
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def VerifyRegisterationOTP(request):
        try:
            u_otp = request.jwt_data["otp"]
            otp = cache.get(f"{request.user.id}_reg_otp")
            cache.delete(f"{request.user.id}_reg_otp")
            if int(u_otp) == int(otp):
                return True
            else:
                return False

        except Exception as e:
            return False


class Oauth_handler:
    @staticmethod
    def generate_secret():
        secret = pyotp.random_base32()
        return secret

    @staticmethod
    def generate_uri(instance, secret):
        uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=instance.email, issuer_name=Site.objects.get_current().domain
        )

        return uri

    @staticmethod
    def verify_otp(user, otp):
        totp = pyotp.TOTP(user.uauth.secret)
        return totp.verify(otp)
