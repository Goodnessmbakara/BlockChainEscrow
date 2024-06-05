from django.urls import path
from .views import (
    BusinessListCreateView,
    BusinessRetrieveUpdateDestroyView,
    InvoiceListCreateView,
    InvoiceRetrieveUpdateDestroyView,
    VerifyBusinessOTPView,OrderListView, BusinessUpdateView
)

urlpatterns = [
    # Business URLs
    path('businesses/', BusinessListCreateView.as_view(), name='business-list-create'),
    path('businesses/<int:pk>/', BusinessRetrieveUpdateDestroyView.as_view(), name='business-retrieve-update-destroy'),
    path('verify-otp/', VerifyBusinessOTPView.as_view(), name='verify-otp'),

    # Invoice URLs
    path('invoices/', InvoiceListCreateView.as_view(), name='invoice-list-create'),
    path('invoices/<int:pk>/', InvoiceRetrieveUpdateDestroyView.as_view(), name='invoice-retrieve-update-destroy'),
    path('orders/', OrderListView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyView.as_view(), name='order-detail'),
    path('business-setting/update/<int:pk>/', BusinessUpdateView.as_view(), name='business-update'),
]