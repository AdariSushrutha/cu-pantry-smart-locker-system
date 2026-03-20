from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import InventoryItem

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'temperature_category', 'quantity', 'unit', 'is_available']
    list_filter = ['temperature_category', 'is_available']
    search_fields = ['name']