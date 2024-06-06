from django.urls import path
from .views import (
    InvoiceListCreateView,OrderRetrieveUpdateDestroyView,
    InvoiceRetrieveUpdateDestroyView,OrderListView,AcceptInvoiceView, DeclineInvoiceView,
)

urlpatterns = [
    path('invoices/', InvoiceListCreateView.as_view(), name='invoice-list-create'),
    path('invoices/<int:pk>/', InvoiceRetrieveUpdateDestroyView.as_view(), name='invoice-retrieve-update-destroy'),
    path('invoice/accept/<int:pk>/', AcceptInvoiceView.as_view(), name='accept-invoice'),
    path('invoice/decline/<int:pk>/', DeclineInvoiceView.as_view(), name='decline-invoice'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyView.as_view(), name='order-detail'),
]