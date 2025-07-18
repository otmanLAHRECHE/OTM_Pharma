from django.shortcuts import render

from otm_users_auth.permissions import IsPharmacist, IsPharmacistAssistant
from stock.models import Medic, DCI, Batch, Famille, Manufacturer, Supplier
from stock.seializers import MedicSerializer, DCISerializer, BatshSerializer, FamilleSerializer, ManufacturerSerializer, SupplierSerializer
from rest_framework import generics
from stock.paginations import MedicPagination

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter



class ManufacturerViewSet(ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'country']
    ordering_fields = ['name']



class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'country']
    ordering_fields = ['name']


class DCIViewSet(ModelViewSet):
    queryset = DCI.objects.all()
    serializer_class = DCISerializer
    filter_backends = [SearchFilter]
    search_fields = ['dci']


class FamilleViewSet(ModelViewSet):
    queryset = Famille.objects.all()
    serializer_class = FamilleSerializer
    filter_backends = [SearchFilter]
    search_fields = ['famille_name']


class MedicViewSet(ModelViewSet):
    queryset = Medic.objects.select_related(
        'medic_famille', 'medic_dci', 'medic_manufact'
    ).all()
    serializer_class = MedicSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    filterset_fields = ['medic_famille', 'medic_dci', 'medic_manufact']
    search_fields = ['forme', 'dosage']
    ordering_fields = ['forme']


class BatchViewSet(ModelViewSet):
    queryset = Batch.objects.select_related('medicine', 'supplier').all()
    serializer_class = BatshSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    filterset_fields = ['medicine', 'supplier', 'expiry_date']
    search_fields = ['barcode']
    ordering_fields = ['expiry_date', 'stock_units', 'price']



