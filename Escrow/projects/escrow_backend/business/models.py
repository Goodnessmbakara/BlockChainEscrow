from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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

class Invoice(models.Model):
    INVOICE_STATUS_CHOICES = [
        ('awaiting_approval', 'Awaiting Approval'),
        ('is_approved', 'Is Approved'),
    ]
    invoice_title = models.CharField(max_length=100)
    invoiceID = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey('Business', on_delete=models.CASCADE)
    sent_to = models.ForeignKey('user_auth.CustomUser', on_delete=models.SET_NULL, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    issued_at = models.DateTimeField()
    current_status = models.CharField(max_length=255, choices=INVOICE_STATUS_CHOICES, default = 'awaiting_approval')

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class InvoiceFinance(models.Model):
    user = models.ForeignKey( 'user_auth.CustomUser', on_delete = models.CASCADE)
    application_reason = models.TextField()
    additional_remark  = models.TextField(null = True, blank=True)

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('payment_success', 'Payment Success'),
        ('shipping_service', 'Shipping Service'),
        ('shipped', 'Shipped'),
        ('awaiting_delivery', 'awaiting_delivery'),
        ('delivered', 'Delivered'),
        
    ]
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
    importer = models.ForeignKey('user_auth.CustomUser', related_name='orders', on_delete=models.CASCADE)
    exporter = models.ForeignKey('Business', on_delete = models.CASCADE, related_name='orders',)
    order_status = models.CharField(max_length = 50, choices=ORDER_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add = True)
    delivery_date = models.DateTimeField(null = True, blank = True)
    total = models.DecimalField(max_digits=10, decimal_places =5)

@receiver(post_save, sender=Invoice)
def create_order_on_invoice_approval(sender, instance, **kwargs):
    if instance.current_status == 'is_approved':
        Order.objects.create(
            invoice=instance,
            title=instance.invoice_title,
            importer=instance.sent_to,
            exporter=instance.creator,
            order_status='payment_success',
            total=instance.total
        )