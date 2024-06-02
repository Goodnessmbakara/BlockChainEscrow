import random
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers
from .models import Invoice, InvoiceItem
from user_auth.models import CustomUser

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'

    def create(self, validated_data):
        business = super().create(validated_data)

        # Generate OTP for email
        email_otp = str(random.randint(100000, 999999))

        # Generate OTP for phone number
        phone_otp = str(random.randint(100000, 999999))

        # Send OTP to email
        subject = 'Business Verification OTP'
        message = f'Your OTP for business email verification is: {email_otp}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [business.official_email]
        send_mail(subject, message, from_email, recipient_list)

        # Send OTP to phone number (you'll need to use a third-party service like Twilio)
        # ...

        # Store the OTPs in the database for later verification
        business.email_otp = email_otp
        business.phone_otp = phone_otp
        business.save()

        return business

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ('id', 'product_name', 'quantity', 'price', 'total')

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = ('id', 'invoiceID', 'created_at', 'creator', 'sent_to', 'amount', 'issued_at', 'current_status', 'items', 'total')

    def get_total(self, obj):
        items = obj.items.all()
        total = sum(item.total for item in items)
        return total

    def create(self, validated_data):
        items_data = self.context.get('view').request.data.get('items')
        invoice = Invoice.objects.create(**validated_data)

        for item_data in items_data:
            quantity = item_data.get('quantity')
            price = item_data.get('price')
            total = quantity * price
            InvoiceItem.objects.create(
                invoice=invoice,
                product_name=item_data.get('product_name'),
                quantity=quantity,
                price=price,
                total=total
            )

        importer_email = self.context.get('view').request.data.get('importer_email')
        if importer_email:
            try:
                user = CustomUser.objects.get(email=importer_email)
                invoice.sent_to = user
                invoice.save()
            except CustomUser.DoesNotExist:
                pass

        return invoice