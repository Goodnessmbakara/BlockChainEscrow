from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

#from rest_framework_social_oauth2.views import GooglePlusAuth
from .views import ( RegisterView, LogoutAPIView, GoogleSocialAuthView,
     VerifyEmail, LoginAPIView, ResendVerificationEmailView, ChangePasswordView)




urlpatterns = [
    path('google/', GoogleSocialAuthView.as_view(), name='google_login'),
    path('signup', RegisterView.as_view(), name="signup"),
    path('signin/', LoginAPIView.as_view(), name="signin"),
    path('signout/', LogoutAPIView.as_view(), name="signout"),
    path('verify-email/', VerifyEmail.as_view(), name="email-verify"),
    path('resend-verification-email/', ResendVerificationEmailView.as_view(), name='resend-verification-email'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
