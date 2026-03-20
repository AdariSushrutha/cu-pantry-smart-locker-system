from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'temperature_category', 'status', 'week_number', 'year', 'created_at']
    list_filter = ['status', 'temperature_category']
    search_fields = ['student__username']