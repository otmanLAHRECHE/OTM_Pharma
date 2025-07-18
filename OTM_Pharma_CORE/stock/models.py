from django.db import models

from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import MinLengthValidator, MinValueValidator
import string
import secrets
from django.core.exceptions import ValidationError
from django.utils.timezone import now
# Create your models here.



class TimeStampedModel(models.Model):
    """
    Abstract base model that provides self-updating created and modified fields.
    
    Attributes:
        created (DateTimeField): When the record was first created (auto-set)
        last_modified (DateTimeField): When the record was last updated (auto-updated)
    """
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    
    class Meta:
        abstract = True


class Manufacturer(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    country = models.CharField(null=True, blank=True, max_length=50)
    address = models.CharField(null=True, blank=True, max_length=50)

    def __str__(self):
        return str(self.name)
    
class Supplier(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    country = models.CharField(null=True, blank=True, max_length=50)
    address = models.CharField(null=True, blank=True, max_length=50)

    def __str__(self):
        return str(self.name)


class DCI(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    dci = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return str(self.dci)
    
class Famille(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    famille_name = models.CharField(unique=True, max_length=70)

    def __str__(self):
        return str(self.famille_name)

class Medic(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    forme = models.CharField(unique=True, max_length=70)
    dosage = models.CharField(max_length=40)
    medic_famille = models.ForeignKey(Famille, on_delete=models.CASCADE, related_name="medicsByFamille")
    medic_dci = models.ForeignKey(DCI, on_delete=models.CASCADE, related_name="medicsByDci")
    medic_manufact = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name="medicsByMnf")

    def __str__(self):
        return str(self.forme)
    
    @property
    def is_available(self):
        """Check if this medicine has any available non-expired stock."""
        return self.batches.filter(stock_units__gt=0).exists()
    
    @property
    def stock(self):
        """Return current inventory level in 'packs:units' format."""
        if self.batches:
            total = sum(batch.stock_units for batch in self.batches.all())
            packs = total // self.units_per_pack
            units = total % self.units_per_pack
            return f"{packs}:{units}"
        return 0
    

def generate_barcode():
    """
    Generate a cryptographically secure 16-digit unique barcode.
    
    Returns:
        str: 16-digit random numeric string
    """
    return ''.join(secrets.choice(string.digits) for _ in range(16))
 
    

class Batch(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    barcode = models.CharField(
        max_length=16,
        unique=True,
        null=True,
        blank=True,
        validators=[MinLengthValidator(16)]
    )
    expiry_date = models.DateField(auto_now=False, auto_now_add=False)
    medicine = models.ForeignKey(Medic, on_delete=models.CASCADE, related_name="batches")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="batches")
    stock_units = models.PositiveIntegerField()
    units_per_pack = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(
        "price in cents",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Price of pack"
    )

    class Meta:
        unique_together = ["expiry_date", "medicine"]

    @property
    def unit_price(self):
        """Calculate and return the price per single unit."""
        return (Decimal(self.price) / Decimal(self.units_per_pack)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP)

    def __str__(self):
        return f"{self.medicine.forme}-{self.expiry_date}"
    
    def clean(self):
        """Validate batch data before saving."""
        super().clean()
        if self.expiry_date and self.expiry_date <= now().date():
            raise ValidationError({"expiry_date": "This is not a valid date"})
        
        if self.stock_units < 0:
            raise ValidationError({"stock_units": "stock units must be positive"})
        
    @property 
    def is_expired(self):
        """Check if this batch has expired."""
        return self.expiry_date <= now().date()
    
    @property 
    def has_amount(self):
        """Check if this batch has any remaining stock."""
        return self.stock_units > 0
    
    @property
    def stock_packets(self):
        """Return inventory level in 'packs:units' format."""
        packs = self.stock_units // self.units_per_pack
        units = self.stock_units % self.units_per_pack
        return f"{packs}:{units}"
    

    def save(self, *args, **kwargs):
        """
        Save the batch, generating a unique barcode if none exists.
        
        The barcode generation ensures uniqueness by checking against existing records.
        """
        if not self.barcode:
            barcode = generate_barcode()
            while Batch.objects.filter(barcode=barcode).exists():
                barcode = generate_barcode()
            self.barcode = barcode

        return super().save(*args, **kwargs)


