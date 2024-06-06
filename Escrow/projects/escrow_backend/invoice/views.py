
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .filters import OrderFilter
from . models import Invoice, Order

from .serializers import InvoiceSerializer,  OrderSerializer

class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.user_type == "importer":
                return Order.objects.filter(importer=user)
            return Order.objects.filter(exporter__owner=user)
        return Order.objects.none()

class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

class InvoiceListCreateView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_class = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.user_type == "importer":
                return Invoice.objects.filter(sent_to=user)
        return Invoice.objects.filter(creator__owner=user)

class InvoiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_class = [IsAuthenticated]

class AcceptInvoiceView(generics.UpdateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        invoice = self.get_object()
        if request.user != invoice.sent_to:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        invoice.current_status = 'is_approved'
        invoice.save()
        return Response({"detail": "Invoice has been accepted."}, status=status.HTTP_200_OK)

class DeclineInvoiceView(generics.UpdateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        invoice = self.get_object()
        if request.user != invoice.sent_to:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        invoice.current_status = 'is_declined'
        invoice.save()
        return Response({"detail": "Invoice has been declined."}, status=status.HTTP_200_OK)