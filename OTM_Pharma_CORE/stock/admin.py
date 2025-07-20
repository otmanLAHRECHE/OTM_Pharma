from django.contrib import admin

from django.contrib.admin import register

from stock.models import Medic, DCI, Batch, Famille, Manufacturer, Supplier

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    search_fields = ['name', 'country']
    ordering = ['name']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    search_fields = ['name', 'country']
    ordering = ['name']


@admin.register(DCI)
class DCIAdmin(admin.ModelAdmin):
    list_display = ['dci']
    search_fields = ['dci']
    ordering = ['dci']


@admin.register(Famille)
class FamilleAdmin(admin.ModelAdmin):
    list_display = ['famille_name']
    search_fields = ['famille_name']
    ordering = ['famille_name']


@admin.register(Medic)
class MedicAdmin(admin.ModelAdmin):
    list_display = ['forme', 'dosage', 'medic_dci', 'medic_famille', 'medic_manufact', 'stock', 'is_available']
    search_fields = ['forme', 'dosage']
    list_filter = ['forme','medic_dci', 'medic_famille', 'medic_manufact']
    ordering = ['forme']


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ['medicine', 'supplier', 'expiry_date', 'stock_units', 'unit_price', 'is_expired', 'has_amount']
    search_fields = ['barcode']
    list_filter = ['supplier', 'expiry_date']
    ordering = ['expiry_date']
