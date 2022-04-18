from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


UserModel = get_user_model()


class CustomBackend(ModelBackend):
    """
        authentication class to login with the email and Phone .
    """
    def authenticate(self, request, username=None, password=None, **kwargs):

        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        if username is None or password is None:
            return

        try:
            user = UserModel.objects.get(Q(phone__exact=username) | Q(email__exact=username))

        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return
        # except UserModel.MultipleObjectsReturned:
        #     user = UserModel.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).order_by('id').first()

        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
