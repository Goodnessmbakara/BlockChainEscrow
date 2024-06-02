
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import isAuthenticated
from rest_framework import status


from . models import Business, Invoice
from user_auth.models import CustomUser

from .serializers import InvoiceSerializer, BusinessSerializer


class BusinessView(generics.ListCreateAPIView):
    serializer_class = BusinessSerializer
    queryset = Business.objects.all()
    
class BusinessDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BusinessSerializer
    queryset = Business.objects.all()

class VerifyBusinessOTPView(APIView):
    def post(self, request):
        business_id = request.data.get('business_id')
        email_otp = request.data.get('email_otp')
        phone_otp = request.data.get('phone_otp')

        try:
            business = Business.objects.get(id=business_id)
        except Business.DoesNotExist:
            return Response({'error': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)

        if business.email_otp == email_otp and business.phone_otp == phone_otp:
            business.contact_verified = True
            business.save()
            return Response({'message': 'Business verified successfully'}, status=status.HTTP_200_OK)
        elif business.email_otp != email_otp:
            return Response({'error': 'Invalid email OTP'}, status=status.HTTP_400_BAD_REQUEST)
        elif business.phone_otp != phone_otp:
            return Response({'error': 'Invalid phone OTP'}, status=status.HTTP_400_BAD_REQUEST)


class InvoiceListCreateView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_class = [isAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.user_type == "importer":
                return Invoice.objects.filter(sent_to=user)
        return Invoice.objects.filter(creator__owner=user)

class InvoiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_class = [isAuthenticated]