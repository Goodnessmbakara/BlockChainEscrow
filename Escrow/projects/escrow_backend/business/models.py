from django.db import models

"""
company_registration_document
proof_of_address (for the business)
articles_of_association
shareholder_certificate
certificate_of_incorporation
financial_statement
bank_statement
tax_document"""

class Business(models.Model):
    owner = models.OneToOneField("user_auth.CustomUser", on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    business_logo = models.ImageField(null = True, blank = True, upload_to = 'business_logos')
    company_registration_number = models.CharField(max_length = 255, null=True, blank=True)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state_origin = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    nearest_landmark = models.CharField(max_length=255, blank=True, null=True)
    official_email = models.EmailField()
    official_number = models.CharField(max_length=255, blank=True, null=True)
    helpdesk_email = models.EmailField(blank=True, null=True)
    helpdesk_number = models.CharField(max_length=255)
    staff_size_range = models.IntegerField()
    kyc_verified = models.BooleanField(default=False)
    contact_verified = models.BooleanField(default=False)
    email_otp = models.CharField(max_length = 20)
    phone_otp = models.CharField(max_length = 20)
