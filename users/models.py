from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from .utils import user_upload_dir

class CustomUser(AbstractUser):
    username            = None
    email               = models.EmailField(verbose_name="email address", unique=True , max_length=60)
    phone               = models.CharField(verbose_name="Phone number" , unique=True , max_length=13)
    first_name          = models.CharField(verbose_name="First Name", max_length=255)
    last_name           = models.CharField(verbose_name="Last Name", max_length=255)
    national_code       = models.CharField(verbose_name="National Code" , unique=True , max_length=13)
    is_phone_verified   = models.BooleanField(verbose_name="Mobile Verification Status",default=False)
    is_email_verified   = models.BooleanField(verbose_name="Email Verification Status",default=False)
    can_trade           = models.BooleanField(verbose_name="User Status",default=False)
    image_file          = models.FileField(verbose_name="Profile Image", upload_to=user_upload_dir, max_length=None)
    ref_code            = models.CharField(verbose_name="Referral Code", max_length=255, blank=True, null=True)

    USERNAME_FIELD      = 'email'
    REQUIRED_FIELDS     = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


    # define the custom permissions
    # related to User.
    class Meta:
         
        permissions = (
            ("user_wait_for_verify", "ثبت نام شده"),
            ("user_blocked", "بلاک شده"),
            ("user_verified", "وریفای شده"),
            ("user_level_2", "سطح دو"),
            )
