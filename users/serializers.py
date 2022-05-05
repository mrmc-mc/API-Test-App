import base64
import io

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.files.base import ContentFile
from django.core.validators import validate_email
from django.utils.timezone import now
from PIL import Image
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import PersonalInfo, UserMedia

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    date_joined = serializers.DateTimeField(read_only=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        exclude = [
            "is_superuser",
            "is_staff",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "is_email_verified": {"read_only": True},
            "is_phone_verified": {"read_only": True},
            "can_trade": {"read_only": True},
            # 'first_name': {'required': True},
            # 'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def validate_password(self, attrs):

        if len(attrs) < 8:
            raise serializers.ValidationError(
                ("This password must contain at least 8 characters."),
                code="password_too_short",
            )

        validate_password(attrs)

        return attrs

    def validate_email(self, attrs):
        validate_email(attrs)
        return attrs

    def validate_phone(self, attrs):

        if not attrs.isdigit():
            raise serializers.ValidationError(
                {"phone": "Phone number must be digits only."}
            )

        if not attrs.startswith("09"):
            raise serializers.ValidationError(
                {"phone": "Phone number must start with 09XXXXXXXX."}
            )

        if len(attrs) != 11:
            raise serializers.ValidationError(
                ("This phone number must contain exactly 11 digits."),
                code="phone_number_invalid",
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        user.save()
        return user


class UserMediaSerializer(serializers.ModelSerializer):

    image_file = serializers.CharField(required=True)

    class Meta:
        model = UserMedia
        fields = fields = ["image_file", "user"]
        extra_kwargs = {
            "user": {"write_only": True},
        }

    def validate_image_file(self, attrs):

        if not attrs.startswith("data:image"):
            raise serializers.ValidationError({"image_file": "Invalid image format."})
        try:
            image = base64.b64decode(attrs.split(",")[1])
            img = Image.open(io.BytesIO(image))
        except Exception:
            raise serializers.ValidationError(
                {"image_file": "file is not valid base64 image"}
            )

        if img.format.lower() not in ["jpg", "jpeg", "png"]:
            raise serializers.ValidationError(
                {"image_file": "Invalid image file format."}
            )

        # width, height = img.size
        # if  not width < 800 and height < 800:
        #     raise serializers.ValidationError(
        #         {"image_file": "image size exceeded, width and height must be less than 800 pixel."})

        return attrs

    def save(self, *args, **kwargs):

        # if isinstance(data, basestring) and data.startswith('data:image'):
        kwargs["image_file"] = ContentFile(
            self.validated_data["image_file"],
            f"{self.initial_data['first_name']}_{self.initial_data['last_name']}-{now()}.txt",
        )
        return super().save(*args, **kwargs)


class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = ["first_name", "last_name", "national_code", "user"]

    def validate_first_name(self, attrs):
        if len(attrs) < 2:
            raise serializers.ValidationError(
                ("This first name must contain at least 2 characters."),
                code="first_name_too_short",
            )

        if not attrs.isalpha():
            raise serializers.ValidationError(
                {"first_name": "First name must be alphabetic only."}
            )

        return attrs

    def validate_last_name(self, attrs):
        if len(attrs) < 2:
            raise serializers.ValidationError(
                ("This last name must contain at least 2 characters."),
                code="last_name_too_short",
            )

        if not attrs.isalpha():
            raise serializers.ValidationError(
                {"last_name": "Last name must be alphabetic only."}
            )

        return attrs

    def validate_national_code(self, attrs):
        if not attrs.isdigit():
            raise serializers.ValidationError(
                {"national_code": "National code must be digits only."}
            )

        if len(attrs) != 10:
            raise serializers.ValidationError(
                ("This national code must contain exactly 10 digits."),
                code="national_code_invalid",
            )
        return attrs

    def create(self, validated_data):
        return super().create(validated_data)


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    Serializer for password change endpoint.
    """

    class Meta:
        model = User
        fields = ["new_password", "old_password"]

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs["new_password"] != self.context["request"].data["re_new_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def validate_old_password(self, attrs):
        user = self.context["request"].user
        if not user.check_password(attrs):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return attrs

    def validate_new_password(self, attrs):

        if len(attrs) < 8:
            raise serializers.ValidationError(
                ("This password must contain at least %(min_length)d characters."),
                code="password_too_short",
                params={"min_length": 8},
            )

        validate_password(attrs)
        return attrs


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "phone",
        )

    def validate_email(self, value):
        user = self.context["request"].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError(
                {"email": "This email is already in use."}
            )
        return value

    def validate_phone(self, value):
        user = self.context["request"].user
        if User.objects.exclude(pk=user.pk).filter(phone=value).exists():
            raise serializers.ValidationError(
                {"phone": "This phone is already in use."}
            )
        return value

    def update(self, instance, validated_data):
        instance.email = validated_data["email"]
        instance.phone = validated_data["phone"]

        instance.save()

        return instance


class UserListSerializer(serializers.ModelSerializer):

    first_name = serializers.PrimaryKeyRelatedField(
        read_only=True, source="uinfo.first_name"
    )
    last_name = serializers.PrimaryKeyRelatedField(
        read_only=True, source="uinfo.last_name"
    )
    national_code = serializers.PrimaryKeyRelatedField(
        read_only=True, source="uinfo.national_code"
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "phone",
            "is_phone_verified",
            "is_email_verified",
            "can_trade",
            "ref_code",
            "first_name",
            "last_name",
            "national_code",
        ]
