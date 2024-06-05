from django.urls import path
from .views import (
    BusinessView,OrderRetrieveUpdateDestroyView,
    BusinessDetailView,
    InvoiceListCreateView,
    InvoiceRetrieveUpdateDestroyView,
    VerifyBusinessOTPView,OrderListView, BusinessUpdateView
)

urlpatterns = [
    # Business URLs
    path('business/', BusinessView.as_view(), name='business-list-create'),
    path('business/<int:pk>/', BusinessDetailView.as_view(), name='business-retrieve-update-destroy'),
    path('update-business/<int:pk>/', BusinessUpdateView.as_view(), name='business-retrieve-update-destroy'),
    path('verify-otp/', VerifyBusinessOTPView.as_view(), name='verify-otp'),

    # Invoice URLs
    path('invoices/', InvoiceListCreateView.as_view(), name='invoice-list-create'),
    path('invoices/<int:pk>/', InvoiceRetrieveUpdateDestroyView.as_view(), name='invoice-retrieve-update-destroy'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyView.as_view(), name='order-detail'),
    path('business-setting/update/<int:pk>/', BusinessUpdateView.as_view(), name='business-update'),
]