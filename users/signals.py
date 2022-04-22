from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.contrib.sites.models import Site
from .utils import EmailThread
from django.conf import settings
from random import randrange
from django.core.cache import cache

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
            user = instance
            otp = randrange(100000,999999)
            cache.set(f"{user.id}_reg_otp", "value", timeout=3600*24*7)
            subject = "ایمیل فعالسازی حساب"
            # email_template_name = "email/auth_email_verify.html"
            index = {
                        "email": user.email,
                    "text":f"TOPKENZ.COM: Your OTP code is: {otp}"
                }
        # body = render_to_string(email_template_name, index)
        
            EmailThread(subject= subject,
                        body=index,
                        sender=settings.DEFAULT_FROM_EMAIL,
                        email= [user.email]).start()

        # except BadHeaderError:
        #     pass
        except:
            pass
