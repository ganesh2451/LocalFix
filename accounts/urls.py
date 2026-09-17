from django.urls import path, include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterView,
    ProviderProfileViewSet,
    AdminProviderViewSet,
    CustomTokenObtainPairView
)

from rest_framework_simplejwt.views import TokenRefreshView


router = DefaultRouter()

router.register(
    'providers',
    ProviderProfileViewSet,
    basename='providers'
)

router.register(
    'admin/providers',
    AdminProviderViewSet,
    basename='admin-providers'
)


urlpatterns = [

    path(
        'register/',
        RegisterView.as_view(),
        name='register'
    ),

    path(
        'login/',
        CustomTokenObtainPairView.as_view(),
        name='login'
    ),

    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

    path(
        '',
        include(router.urls)
    ),
]