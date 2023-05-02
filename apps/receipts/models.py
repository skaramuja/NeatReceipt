from django.db import models
from neatreceipt import settings


class ReceiptImage(models.Model):
    """
    Model representing a receipt image.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    image = models.ImageField(upload_to='receipts')

    def __str__(self):
        return str(self.id)


class Vendor(models.Model):
    """
    Model for the vendor.
    """
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=150)


class Receipt(models.Model):
    """
    Model for a receipt.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    image = models.ForeignKey(ReceiptImage, on_delete=models.CASCADE,)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateField(auto_now_add=True)
    date = models.DateTimeField(auto_now_add=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,)


class ReceiptItem(models.Model):
    """
    Model for an item on a receipt.
    """
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE,)
    type = models.CharField(max_length=150)
