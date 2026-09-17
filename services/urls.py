from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ServiceCategoryViewSet, ServiceViewSet


router = DefaultRouter()

router.register('categories', ServiceCategoryViewSet)
router.register('services', ServiceViewSet)


urlpatterns = [
    path('', include(router.urls)),
]