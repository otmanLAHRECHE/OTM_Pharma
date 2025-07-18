from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ManufacturerViewSet, SupplierViewSet, DCIViewSet,
    FamilleViewSet, MedicViewSet, BatchViewSet
)



router = DefaultRouter()
router.register(r'manufacturers', ManufacturerViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'dcis', DCIViewSet)
router.register(r'familles', FamilleViewSet)
router.register(r'medics', MedicViewSet)
router.register(r'batches', BatchViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]