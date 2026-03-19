from django.db import models

# Create your models here.
from django.db import models

class InventoryItem(models.Model):

    TEMPERATURE_CHOICES = [
        ('frozen', 'Frozen'),
        ('refrigerated', 'Refrigerated'),
        ('ambient', 'Ambient'),
    ]

    name = models.CharField(max_length=255)
    temperature_category = models.CharField(max_length=20, choices=TEMPERATURE_CHOICES)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=50, default='item')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.temperature_category}) - Qty: {self.quantity}"