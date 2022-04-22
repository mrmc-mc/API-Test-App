# Tools

from django.conf import settings
import jwt

from django.core.mail import send_mail
import threading


def user_upload_dir(instance , filename):
    """  set upload directroy by user id and change file name   """

    return f'user_{instance.national_code}/{filename}'


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


class EmailThread(threading.Thread):

        def __init__(self, subject, body, sender, email):
                self.subject = subject
                self.body = body
                self.sender = sender
                self.email = email
                threading.Thread.__init__(self)



        def run(self):
                """ send an email """

                try:

                        send_mail(subject= self.subject,
                                message=None,
                                html_message=self.body,
                                from_email= self.sender,
                                recipient_list= self.email, 
                                fail_silently=False)

                        return True

                except Exception as e:
                        return False