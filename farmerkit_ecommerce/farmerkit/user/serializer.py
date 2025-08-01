from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password,mask_hash
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = [
            'id', 'name', 'email', 'password', 'phone','created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ('created_at', 'updated_at', 'is_active')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.pop('password'))
        validated_data['is_active'] = True
        return super().create(validated_data)
    

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password",]  
    
class UserViewAndUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['name'] = user.name  
        token['id'] = user.id
        return token
    
class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(min_length=6)