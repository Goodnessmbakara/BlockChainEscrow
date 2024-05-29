from django.db import models

class Business(models.Model):
    business_name = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state_origin = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    nearest_landmark = models.CharField(max_length=255, blank=True, null=True)
    official_email = models.EmailField(blank=True, null=True)
    official_number = models.CharField(max_length=255, blank=True, null=True)
    helpdesk_email = models.EmailField(blank=True, null=True)
    helpdesk_number = models.CharField(max_length=255, blank=True, null=True)
    staff_size = models.IntegerField()

class User(models.Model):
    USER_TYPE_CHOICES = [
        ('experter', 'Experter'),
        ('importer', 'Importer'),
    ]
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=255, choices=USER_TYPE_CHOICES)
    

class KYC(models.Model):
    is_successful = models.BooleanField(default=False)
    business = models.OneToOneField(Business, on_delete=models.CASCADE)

class Order(models.Model):
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    status = models.CharField(max_length=255)

class Notification(models.Model):
    message_body = models.TextField()
    is_read = models.BooleanField(default=False)

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('awaiting', 'Awaiting'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('payment_success', 'Payment Success'),
        ('is_approved', 'Is Approved'),
        ('shipping_service', 'Shipping Service')
    ]
    invoiceID = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.CharField(max_length=255)
    sent_to = models.ForeignKey(Business, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    issued_at = models.DateTimeField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    current_status = models.CharField(max_length=255, choices=STATUS_CHOICES)

class Wallet(models.Model):
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2)
    escrow = models.DecimalField(max_digits=10, decimal_places=2)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

class Dispute(models.Model):
    description = models.TextField()
    files = models.FileField(upload_to='dispute_files/')
    
