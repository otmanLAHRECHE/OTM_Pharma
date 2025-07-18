from rest_framework import serializers 
from stock.models import Medic, DCI, Batch, Famille, Manufacturer, Supplier
from django.utils.timezone import now 


class SupplierSerializer(serializers.ModelSerializer):
    """Serializer for Supplier model (read/write)."""
    class Meta:
        model = Supplier
        fields = ["id", "name", "address", "city"]

class ManufacturerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manufacturer
        fields = ["id", "name", "address", "city"]

class DCISerializer(serializers.ModelSerializer):

    class Meta:
        model = DCI
        fields = ["id", "dci"]

class FamilleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Famille
        fields = ["id", "famille_name"]


class MedicSerializer(serializers.ModelSerializer):

    medic_famille = FamilleSerializer()
    medic_dci = DCISerializer()
    medic_manufact = ManufacturerSerializer()

    class Meta:
        model = Medic
        fields = ["id", "forme", "dosage", "medic_famille", "medic_dci", "medic_manufact"]




class BatshSerializer(serializers.ModelSerializer):

    medicine = MedicSerializer()
    supplier = SupplierSerializer()

    class Meta:
        model = Batch
        fields = ["id", "barcode", "expiry_date", "medicine", "supplier", "stock_units", "units_per_pack", "price"]

