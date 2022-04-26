from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from .models import PersonalInfo
from django.core.files.base import ContentFile


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
 
    date_joined = serializers.DateTimeField(read_only=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    image_file = serializers.CharField()  
 
    class Meta:
        model = User
        exclude = ['is_superuser', 'is_staff',]
        extra_kwargs = {
                'password': {'write_only': True},
                'is_email_verified': {'read_only': True},
                'is_phone_verified': {'read_only': True},
                'can_trade': {'read_only': True},
                'first_name': {'required': True},
                'last_name': {'required': True}
            }


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs


    # def validate_image_file(self, value):
    #     value = ContentFile(value,
    #                 f"{self.validated_data['first_name']}_{self.validated_data['last_name']}-{now()}.txt")
    #     return value

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        user.save()    
        return user

    def save(self, *args, **kwargs):
        # if isinstance(data, basestring) and data.startswith('data:image'):
            kwargs['image_file'] = ContentFile(self.validated_data['image_file'],
                        f"{self.validated_data['first_name']}_{self.validated_data['last_name']}-{now()}.txt")
            return super().save(*args, **kwargs)


class PersonalInfoSerializer(serializers.ModelSerializer):

    # user = UserSerializer(read_only=True)
    user = serializers.RelatedField(read_only=True)
    class Meta:
        model = PersonalInfo
        fields=['first_name', 'last_name', 'national_code', 'user'] 


    def create(self, validated_data):
        validated_data['user'] = self.user

        return super().create(validated_data)




class ChangePasswordSerializer(serializers.ModelSerializer):
    
    class Meta:
            model = User
            fields = ['new_password', 'old_password']
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != self.context['request'].data['re_new_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value


# class ChangePasswordSerializer(serializers.ModelSerializer):
#     old_password = serializers.CharField(required=True, write_only=True)
#     new_password = serializers.CharField(required=True, write_only=True)
#     re_new_password = serializers.CharField(required=True, write_only=True)

#     def update(self, instance, validated_data):

#         instance.password = validated_data.get('password', instance.password)

#         if not validated_data['new_password']:
#               raise serializers.ValidationError({'new_password': 'not found'})

#         if not validated_data['old_password']:
#               raise serializers.ValidationError({'old_password': 'not found'})

#         if not instance.check_password(validated_data['old_password']):
#               raise serializers.ValidationError({'old_password': 'wrong password'})

#         if validated_data['new_password'] != validated_data['re_new_password']:
#             raise serializers.ValidationError({'passwords': 'passwords do not match'})

#         if validated_data['new_password'] == validated_data['re_new_password'] and instance.check_password(validated_data['old_password']):
#             instance.set_password(validated_data['new_password'])
#             instance.save()
#             return instance

#     class Meta:
#         model = User
#         fields = ['old_password', 'new_password','re_new_password']



class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'national_code', 'ref_code')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']

        instance.save()

        return instance