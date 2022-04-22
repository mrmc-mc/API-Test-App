from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from .models import PersonalInfo

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
 
    date_joined = serializers.ReadOnlyField()
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
 
    class Meta:
        model = User
        exclude = ['is_email_verified', 'is_phone_verified', 'can_trade']
        extra_kwargs = {'password': {'write_only': True},
                'first_name': {'required': True},
                'last_name': {'required': True}
        }


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs


    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        user.save()    
        return user


class PersonalInfoSerializer(serializers.ModelSerializer):

    # user = UserSerializer(read_only=True)
    user = serializers.RelatedField(read_only=True)
    class Meta:
        model = PersonalInfo
        fields=['first_name', 'last_name', 'national_code', 'user'] 


    def create(self, validated_data):
        validated_data['user'] = self.user

        return super().create(validated_data)