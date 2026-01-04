import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer, EmailVerificationSerializer, LoginSerializer, OTPVerificationSerializer

logger = logging.getLogger(__name__)

class SignupView(APIView):
    def post(self, request):
        try:
            logger.info(f"Signup request data: {request.data}")
            serializer = SignupSerializer(data=request.data)
            if serializer.is_valid():
                logger.info("Serializer is valid, saving...")
                serializer.save()
                logger.info("Signup successful")
                return Response({'message': 'Signup successful. Check your email for verification code.'}, status=status.HTTP_201_CREATED)
            logger.warning(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Signup error: {str(e)}", exc_info=True)
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EmailVerificationView(APIView):
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message': 'Login initiated. Check your email for OTP.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OTPVerificationView(APIView):
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
