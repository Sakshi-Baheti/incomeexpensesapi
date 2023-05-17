from attr import validate
from rest_framework import serializers
from .models import User 
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=70, min_length=8, write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
       
        username = attrs.get('username', '')
        email = attrs.get('email', '')

        if not username.isalnum():
            raise serializers.ValidationError("Username should only contain Alphanumberic characters!")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class EmailVerifySerializer(serializers.ModelSerializer):
    token = serializers.CharField()

    class Meta:
        model = User
        fields = ['token']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255,
                                   min_length=3)
    password = serializers.CharField(max_length=70,
                                     min_length=8,
                                     write_only=True)
    username = serializers.CharField(max_length=255,
                                   min_length=3,
                                   read_only=True)
    tokens = serializers.CharField(read_only=True)

    class Meta:
         model = User
         fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')
        user=auth.authenticate(email=email, password=password)
        print("--USER--", user)
        if not user:
            raise AuthenticationFailed('Invalid Credentials, Try Again.')
        
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact Admin.')
        
        if not user.is_verified:
            raise AuthenticationFailed('Email not verified!')
        
        
        
        return {
            'email' : user.email,
            'username' : user.username,
            # 'tokens' : User.tokens()
            'tokens' : user.tokens
        }

class PasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=3)
    class Meta:
        fields = ['email']

class SetNewPasswordSerializer(serializers.Serializer):
        password = serializers.CharField(max_length=70, min_length=8, write_only=True)
        token = serializers.CharField(min_length=1, write_only=True)
        uidb64 = serializers.CharField(min_length=1, write_only=True)

        class Meta:
            fields = ['password', 'token', 'uidb64']

        def validate(self, attrs):
            try:
                password = attrs.get('password')
                token = attrs.get('token')
                uidb64 = attrs.get('uidb64')
                id = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(id=id)
                if not PasswordResetTokenGenerator().check_token(user, token):
                    raise AuthenticationFailed('The reset link is invalid!', 401)
            
                user.set_password(password)
                user.save()
                return user
            except Exception as e :
                    raise AuthenticationFailed('The reset link is invalid!', 401)
            return super().validate(attrs)