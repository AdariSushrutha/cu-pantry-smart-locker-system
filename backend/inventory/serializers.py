from rest_framework import serializers
from .models import InventoryItem


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = [
            'id',
            'name',
            'barcode',
            'category',
            'quantity',
            'unit',
            'is_available',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']