from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    SignupSerializer,
    EmailVerificationSerializer,
    LoginSerializer,
    OTPVerificationSerializer,
)

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Signup successful. OTP sent."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationView(APIView):
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Email verified"}, status=200)
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "OTP sent"}, status=200)
        return Response(serializer.errors, status=400)


class OTPVerificationView(APIView):
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Login success"}, status=200)
        return Response(serializer.errors, status=400)
