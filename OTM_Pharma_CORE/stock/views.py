from django.shortcuts import render

from otm_users_auth.permissions import IsPharmacist, IsPharmacistAssistant
from stock.models import Medic, DCI, Batch, Famille, Manufacturer, Supplier
from stock.seializers import MedicSerializer, DCISerializer, BatshSerializer, FamilleSerializer, ManufacturerSerializer, SupplierSerializer, MedicRetrieveSerializer, MedicInSerializer
from rest_framework import generics
from stock.paginations import MedicPagination
from rest_framework.filters import SearchFilter


class DCIListCreateAPIView(generics.ListCreateAPIView):
    """API endpoint for listing and creating DCI"""
    permission_classes = [IsPharmacist, IsPharmacistAssistant]
    queryset = DCI.objects.all()
    serializer_class = DCISerializer



class FamilleListCreateAPIView(generics.ListCreateAPIView):
    """API endpoint for listing and creating Famille"""
    permission_classes = [IsPharmacist, IsPharmacistAssistant]
    queryset = Famille.objects.all()
    serializer_class = FamilleSerializer


class ManufacturerListCreateAPIView(generics.ListCreateAPIView):
    """API endpoint for listing and creating Mnf"""
    permission_classes = [IsPharmacist, IsPharmacistAssistant]
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer


class SupplierListCreateAPIView(generics.ListCreateAPIView):
    """API endpoint for listing and creating Supplier"""
    permission_classes = [IsPharmacist, IsPharmacistAssistant]
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class MedicListCreateAPIView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating Medicines.
    
    Features:
    - Search functionality
    - Custom pagination
    - Different serializers for GET vs POST
    """
    permission_classes = [IsPharmacist, IsPharmacistAssistant]
    filter_backends = [SearchFilter]
    search_fields = ['forme', 'medic_dci', 'medic_famille']
    pagination_class = MedicPagination
    queryset = Medic.objects.select_related("medic_dci", "medic_famille")

    def get_serializer_class(self):
        if self.request.method == "GET":
            return MedicRetrieveSerializer
        return MedicInSerializer