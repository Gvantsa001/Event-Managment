from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from accounts.models import User
from accounts.utils import send_normal_email

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=64, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=64, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")

        if password != password2:
            raise serializers.ValidationError("Passwords do not match")

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )

        return user

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=155, min_length=6)
    password = serializers.CharField(max_length=68, write_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'full_name', 'access_token', 'refresh_token']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get("password")
        request = self.context.get("request")
        user = authenticate(request, username=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials')

        if not user.is_verified:
            raise AuthenticationFailed('Email not verified')

        tokens = user.tokens()
        return {
            'email': user.email,
            'full_name': user.get_full_name(),
            'access_token': str(tokens.get("access")),
            'refresh_token': str(tokens.get("refresh"))
        }

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email does not exist")

        user = User.objects.get(email=email)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)
        request = self.context.get('request')
        current_site = get_current_site(request).domain
        relative_link = reverse('reset-password-confirm', kwargs={'uidb64': uidb64, 'token': token})
        abslink = f"http://{current_site}{relative_link}"
        email_body = f"Hello {user}, use this link to reset your password: {abslink}"
        data = {
            'email_body': email_body,
            'email_subject': 'Password Reset Request',
            'to_email': user.email,
        }
        send_normal_email(data)

        return super().validate(attrs)

