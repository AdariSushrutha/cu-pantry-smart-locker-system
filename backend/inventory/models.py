from django.db import models


class InventoryItem(models.Model):

    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('hygiene', 'Hygiene'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=50, null=True, blank=True, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='food')
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=50, default='item')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.temperature_category}) - Qty: {self.quantity}"