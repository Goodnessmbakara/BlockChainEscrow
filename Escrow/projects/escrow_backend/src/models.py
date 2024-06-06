from django.db import models

class Order(models.Model):
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    status = models.CharField(max_length=255)

class Notification(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField()
    is_read = models.BooleanField(default=False)


class Wallet(models.Model):
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2)
    escrow = models.DecimalField(max_digits=10, decimal_places=2)
    business = models.ForeignKey('business.Business', on_delete=models.CASCADE)

class Dispute(models.Model):
    description = models.TextField()
    files = models.FileField(upload_to='dispute_files/')
    
