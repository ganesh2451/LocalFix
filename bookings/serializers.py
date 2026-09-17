from rest_framework import serializers
from .models import ServiceRequest, Review


class ServiceRequestSerializer(serializers.ModelSerializer):

    customer_name = serializers.CharField(
        source='customer.username',
        read_only=True
    )

    provider_name = serializers.CharField(
        source='provider.user.username',
        read_only=True
    )

    service_name = serializers.CharField(
        source='service.name',
        read_only=True
    )

    class Meta:
        model = ServiceRequest

        fields = [
            'id',
            'customer',
            'customer_name',
            'provider',
            'provider_name',
            'service',
            'service_name',
            'problem_description',
            'preferred_date',
            'address',
            'status',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'customer',
            'status',
            'created_at',
            'updated_at',
        ]


class ReviewSerializer(serializers.ModelSerializer):

    customer_name = serializers.CharField(
        source='customer.username',
        read_only=True
    )

    provider_name = serializers.CharField(
        source='provider.user.username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = [
            'id',
            'service_request',
            'customer',
            'customer_name',
            'provider',
            'provider_name',
            'rating',
            'comment',
            'created_at',
        ]

        read_only_fields = [
            'customer',
            'provider',
            'created_at',
        ]