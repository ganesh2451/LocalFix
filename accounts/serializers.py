from rest_framework import serializers
from .models import User, ProviderProfile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'role',
        )

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'CUSTOMER')
        )

        return user


class ProviderProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    email = serializers.EmailField(
        source='user.email',
        read_only=True
    )

    service_names = serializers.SerializerMethodField()

    class Meta:
        model = ProviderProfile

        fields = [
            'id',
            'user',
            'username',
            'email',
            'phone',
            'address',
            'experience_years',
            'is_verified',
            'services',
            'service_names',
        ]

        extra_kwargs = {
            'services': {
                'required': False
            }
        }

        read_only_fields = [
            'user',
            'is_verified',
        ]

    def get_service_names(self, obj):
        return [
            service.name
            for service in obj.services.all()
        ]