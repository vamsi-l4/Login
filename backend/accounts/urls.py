from django.urls import path
from .views import SignupView, EmailVerificationView, LoginView, OTPVerificationView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('verify-email/', EmailVerificationView.as_view(), name='verify_email'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-otp/', OTPVerificationView.as_view(), name='verify_otp'),
]
