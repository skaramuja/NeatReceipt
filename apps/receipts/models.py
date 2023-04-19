import pathlib

from django.db import models


class ReceiptUpload(models.Model):
    category = models.CharField(max_length=30)
    image = models.ImageField(upload_to='static/img/receipts')

