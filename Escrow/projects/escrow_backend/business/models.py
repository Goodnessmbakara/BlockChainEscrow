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
    staff_size = models.IntegerField()
    kyc_verified = models.BooleanField(default=False)
    contact_verified = models.BooleanField(default=False)
    email_otp = models.CharField(max_length = 20)
    phone_otp = models.CharField(max_length = 20)

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('awaiting_approval', 'Awaiting Approval'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('payment_success', 'Payment Success'),
        ('is_approved', 'Is Approved'),
        ('shipping_service', 'Shipping Service')
    ]
    
    invoiceID = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey('Business', on_delete=models.CASCADE)
    sent_to = models.ForeignKey('user_auth.CustomUser', on_delete=models.SET_NULL, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    issued_at = models.DateTimeField()
    current_status = models.CharField(max_length=255, choices=STATUS_CHOICES, default = 'awaiting_approval')

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)