from rest_framework import serializers
from django.contrib.auth import get_user_model
 
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
 
    date_joined = serializers.ReadOnlyField()
    
 
    class Meta(object):
        model = User
        exclude = ['is_email_verified', 'is_phone_verified', 'can_trade']
        extra_kwargs = {'password': {'write_only': True}}