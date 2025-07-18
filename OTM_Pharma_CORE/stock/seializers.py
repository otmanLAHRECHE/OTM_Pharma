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


class MedicInSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medic
        fields = ["id",
                   "forme",
                     "dosage",
                       "medic_famille",
                         "medic_dci",
                           "medic_manufact"]


class MedicRetrieveSerializer(serializers.ModelSerializer):
    medic_dci = serializers.StringRelatedField()
    medic_famille = serializers.StringRelatedField()
    medic_manufact = serializers.StringRelatedField()
    barcodes = serializers.SerializerMethodField()

    def get_barcodes(self, obj):
        """Get all barcodes associated with this medicine's batches."""
        barcodes = obj.batches.values_list("barcode", flat=True)
        return list(barcodes)
    
    class Meta:
        model = Medic
        fields = ["id",
                   "forme",
                     "dosage",
                       "medic_famille",
                         "medic_dci",
                           "medic_manufact",
                                "barcodes",]
        
        read_only_fields = ["barcodes"]


class BatshSerializer(serializers.ModelSerializer):

    medicine = MedicSerializer()
    supplier = SupplierSerializer()

    class Meta:
        model = Batch
        fields = ["id", "barcode", "expiry_date", "medicine", "supplier", "stock_units", "units_per_pack", "price"]


class BatshInSerializer(serializers.ModelSerializer):

    medicine = MedicSerializer()
    supplier = SupplierSerializer()

    class Meta:
        model = Batch
        fields = ["id", "barcode", "expiry_date", "medicine", "supplier", "stock_units", "units_per_pack", "price"]