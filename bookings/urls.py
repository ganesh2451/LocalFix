from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ServiceRequestViewSet, ReviewViewSet


router = DefaultRouter()

router.register(
    'requests',
    ServiceRequestViewSet,
    basename='requests'
)

router.register(
    'reviews',
    ReviewViewSet,
    basename='reviews'
)


urlpatterns = [
    path('', include(router.urls)),
]