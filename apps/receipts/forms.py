from django import forms
from .models import ReceiptImage


class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = ReceiptImage
        fields = ('image',)
