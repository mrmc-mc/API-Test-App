from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from .utils import Email, Oauth_handler
from django.conf import settings
from .models import OauthInfo

def create_group(sender, **kwargs):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    from django.contrib.auth.models import Group
    from django.contrib.auth.models import Permission

    ngp_list = ['registered_group','verified_group','level2_group' , "blocked_group"]

    ngp_perm = {'registered_group':["user_wait_for_verify"], "verified_group":["user_verified"],
                 "blocked_group":["user_blocked"] ,
                 "level2_group":["user_verified","user_level_2"]}

    current_group = Group.objects.all()

    cgp_list = [ gp.name for gp in current_group]

    for newgp in ngp_list:

        if newgp not in cgp_list:
            new_group = Group.objects.create(name=newgp)

            for perm in ngp_perm[newgp]:
                perms = Permission.objects.get(codename=perm)
                new_group.permissions.add(perms)

            new_group.save()




def sendOTP_after_registration(sender, instance, created, **kwargs):
    """ Send unique code to user email """

    if created:
        try:
            Email.SendRegisterationOTP(instance=instance)
            return True
            print("*"*90)
        except:
            print("-"*90)
            print(e)
            print("-"*90)


def OauthGenerator(sender, instance, created, **kwargs):
    """ Generate secret and uri Auth for user """

    if created:
        try:
            secret = Oauth_handler.generate_secret()
            uri = Oauth_handler.generate_uri(instance=instance,secret=secret)
            auth = OauthInfo.objects.create(user=instance,secret=secret, uri=uri)
            auth.save()
            print(auth)
        except Exception as e:
            print("="*90)
            print(e)
            print("="*90)
