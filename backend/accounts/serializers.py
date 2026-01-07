from rest_framework import serializers
from django.utils import timezone
from django.db import IntegrityError
from django.core.mail import send_mail
from django.conf import settings
from .models import User
import random
from datetime import timedelta

class SignupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True, max_length=150)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["name", "email", "password"]

    def create(self, validated_data):
        name = validated_data.pop("name")
        password = validated_data.pop("password")

        try:
            user = User.objects.create(
                username=name,
                email=validated_data["email"],
            )
            user.set_password(password)

            user.otp = str(random.randint(100000, 999999))
            user.otp_created_at = timezone.now()
            user.save()

            # Send OTP email
            # send_mail(
            #     'Your OTP Code',
            #     f'Your OTP code is {user.otp}. It expires in 10 minutes.',
            #     settings.DEFAULT_FROM_EMAIL,
            #     [user.email],
            #     fail_silently=True,
            # )

            return user
        except IntegrityError as e:
            if 'email' in str(e):
                raise serializers.ValidationError("A user with this email already exists.")
            elif 'username' in str(e):
                raise serializers.ValidationError("A user with this name already exists.")
            else:
                raise serializers.ValidationError("A user with this email or name already exists.")


class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        user = User.objects.filter(email=data["email"]).first()
        if not user:
            raise serializers.ValidationError("User not found")

        if user.otp != data["otp"]:
            raise serializers.ValidationError("Invalid OTP")

        if user.otp_created_at < timezone.now() - timedelta(minutes=10):
            raise serializers.ValidationError("OTP expired")

        user.email_verified = True
        user.otp = None
        user.save()
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(email=data["email"]).first()
        if not user or not user.check_password(data["password"]):
            raise serializers.ValidationError("Invalid credentials")

        user.otp = str(random.randint(100000, 999999))
        user.otp_created_at = timezone.now()
        user.save()

        # Send OTP email
        # send_mail(
        #     'Your Login OTP Code',
        #     f'Your login OTP code is {user.otp}. It expires in 10 minutes.',
        #     settings.DEFAULT_FROM_EMAIL,
        #     [user.email],
        #     fail_silently=True,
        # )

        return data


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        user = User.objects.filter(email=data["email"]).first()
        if not user:
            raise serializers.ValidationError("User not found")

        if user.otp != data["otp"]:
            raise serializers.ValidationError("Invalid OTP")

        if user.otp_created_at < timezone.now() - timedelta(minutes=10):
            raise serializers.ValidationError("OTP expired")

        user.otp = None
        user.save()
        return data
