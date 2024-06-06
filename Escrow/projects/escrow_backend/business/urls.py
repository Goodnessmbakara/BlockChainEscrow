from django.urls import path
from .views import (
    BusinessView,
    BusinessDetailView,
    VerifyBusinessOTPView, BusinessUpdateView
)

urlpatterns = [
    # Business URLs
    path('business/', BusinessView.as_view(), name='business-list-create'),
    path('business/<int:pk>/', BusinessDetailView.as_view(), name='business-retrieve-update-destroy'),
    path('update-business/<int:pk>/', BusinessUpdateView.as_view(), name='business-retrieve-update-destroy'),
    path('verify-otp/', VerifyBusinessOTPView.as_view(), name='verify-otp'),
    path('business-setting/update/<int:pk>/', BusinessUpdateView.as_view(), name='business-update'),
]