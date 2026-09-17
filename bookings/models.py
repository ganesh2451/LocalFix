from django.db import models
from accounts.models import User, ProviderProfile
from services.models import Service


class ServiceRequest(models.Model):

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
    )

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='service_requests'
    )

    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        related_name='service_requests'
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='service_requests'
    )

    problem_description = models.TextField()

    preferred_date = models.DateField()

    address = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request #{self.id} - {self.status}"

class Review(models.Model):

    service_request = models.OneToOneField(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name='review'
    )

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews_given'
    )

    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        related_name='reviews_received'
    )

    rating = models.PositiveIntegerField()

    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for Request #{self.service_request.id}"