from django.db import models

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

    class Meta:
        abstract = True


class cls(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, null=False, blank=False)
    

