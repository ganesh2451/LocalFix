from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('CUSTOMER', 'Customer'),
        ('PROVIDER', 'Provider'),
        ('ADMIN', 'Admin'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='CUSTOMER'
    )

    def __str__(self):
        return f"{self.username} - {self.role}"


class ProviderProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='provider_profile'
    )

    phone = models.CharField(max_length=15)

    address = models.TextField()

    experience_years = models.PositiveIntegerField(default=0)

    is_verified = models.BooleanField(default=False)

    services = models.ManyToManyField(
        'services.Service',
        related_name='providers'
    )

    def __str__(self):
        return self.user.username