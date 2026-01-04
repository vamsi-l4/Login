from rest_framework import serializers
from django.utils import timezone
from django.db import IntegrityError
from .models import User
import random
from datetime import timedelta

class SignupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["name", "email", "password"]

    def validate_name(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this name already exists.")
        return value

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

            return user
        except IntegrityError:
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
