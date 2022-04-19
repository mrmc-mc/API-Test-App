

def create_group(sender, **kwargs):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    from django.contrib.auth.models import Group
    from django.contrib.auth.models import Permission

    ngp_list = ['registered_group','verified_group','level2_group' , "blocked_group"]

    ngp_perm = {'registered_group':["user_wait_for_verify"] , "verified_group":["user_verified"] , "blocked_group":["user_blocked"] ,
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
