from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('admin', 'Admin'),
        ('supplier', 'Supplier'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username


class SupplierProfile(models.Model):
    """Additional information for supplier accounts."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="supplier_profile",
    )
    company_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.company_name
