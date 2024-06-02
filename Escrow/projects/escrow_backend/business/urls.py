from django.urls import path
from .views import (
    BusinessListCreateView,
    BusinessRetrieveUpdateDestroyView,
    InvoiceListCreateView,
    InvoiceRetrieveUpdateDestroyView,
    VerifyOTPView,
)

urlpatterns = [
    # Business URLs
    path('businesses/', BusinessListCreateView.as_view(), name='business-list-create'),
    path('businesses/<int:pk>/', BusinessRetrieveUpdateDestroyView.as_view(), name='business-retrieve-update-destroy'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),

    # Invoice URLs
    path('invoices/', InvoiceListCreateView.as_view(), name='invoice-list-create'),
    path('invoices/<int:pk>/', InvoiceRetrieveUpdateDestroyView.as_view(), name='invoice-retrieve-update-destroy'),
]