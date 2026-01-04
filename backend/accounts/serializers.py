from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import User
import random
from datetime import timedelta

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']



    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        otp = str(random.randint(100000, 999999))
        user.otp = otp
        user.otp_created_at = timezone.now()
        user.save()
        send_mail(
            'Email Verification',
            f'Your verification code is {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return user

class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        data['otp'] = data['otp'].strip()
        try:
            user = User.objects.get(email=data['email'])
            if user.otp == data['otp'] and user.otp_created_at > timezone.now() - timedelta(minutes=10):
                user.email_verified = True
                user.otp = None
                user.save()
                return data
            raise serializers.ValidationError('Invalid or expired OTP')
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found')

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
            if user.check_password(data['password']) and user.email_verified:
                otp = str(random.randint(100000, 999999))
                user.otp = otp
                user.otp_created_at = timezone.now()
                user.save()
                send_mail(
                    'Login OTP',
                    f'Your login OTP is {otp}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                return data
            raise serializers.ValidationError('Invalid credentials or email not verified')
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found')

class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
            if user.otp == data['otp'] and user.otp_created_at > timezone.now() - timedelta(minutes=10):
                user.otp = None
                user.save()
                return data
            raise serializers.ValidationError('Invalid or expired OTP')
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found')
