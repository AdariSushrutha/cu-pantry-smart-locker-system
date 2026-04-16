from django.contrib import admin
from .models import InventoryItem


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'quantity', 'unit', 'is_available']
    list_filter = ['category', 'is_available']
    search_fields = ['name']