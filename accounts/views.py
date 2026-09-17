from django.db.migrations import serializer
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, ProviderProfile
from .serializers import RegisterSerializer, ProviderProfileSerializer
from .permissions import IsProvider, IsAdmin


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):

        token = super().get_token(user)

        token['role'] = user.role
        token['username'] = user.username

        return token

class CustomTokenObtainPairView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ProviderProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderProfileSerializer
    permission_classes = [IsAuthenticated, IsProvider]

    def get_queryset(self):
        return ProviderProfile.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        detail=False,
        methods=['get'],
        url_path='by-service/(?P<service_id>[^/.]+)',
        permission_classes=[IsAuthenticated]
    )
    def by_service(self, request, service_id=None):
        providers = ProviderProfile.objects.filter(
            services__id=service_id,
            is_verified=True
        ).distinct()

        serializer = self.get_serializer(providers, many=True)

        return Response(serializer.data)

class AdminProviderViewSet(viewsets.ModelViewSet):

    serializer_class = ProviderProfileSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return ProviderProfile.objects.all()

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated, IsAdmin]
    )
    def verify(self, request, pk=None):

        provider = self.get_object()

        provider.is_verified = True
        provider.save()

        return Response({
            'message': 'Provider verified successfully.',
            'provider': provider.user.username,
            'is_verified': provider.is_verified
        })