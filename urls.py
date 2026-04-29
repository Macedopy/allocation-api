from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import TruckViewSet, LoadViewSet, AllocationViewSet

router = DefaultRouter()
router.register(r'trucks', TruckViewSet)
router.register(r'loads', LoadViewSet)
router.register(r'run-allocation', AllocationViewSet, basename='allocation')

urlpatterns = [
    path('', include(router.urls)),
]
