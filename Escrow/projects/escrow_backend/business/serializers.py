import random
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers
from .models import Business


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

class BusinessUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = [
            'business_logo',
            'helpdesk_email',
            'helpdesk_number',
            'staff_size_range'
        ]
    