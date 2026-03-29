from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'temperature_category', 'status', 'requires_lower_locker', 'week_number', 'year', 'created_at']
    list_filter = ['status', 'temperature_category', 'requires_lower_locker']
    search_fields = ['student__username']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'inventory_item', 'created_at']
    search_fields = ['order__id', 'inventory_item__name']