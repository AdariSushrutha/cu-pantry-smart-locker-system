from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Locker, TemperatureLog

@admin.register(Locker)
class LockerAdmin(admin.ModelAdmin):
    list_display = ['locker_number', 'temperature_type', 'status', 'current_order']
    list_filter = ['status', 'temperature_type']
    search_fields = ['locker_number']

@admin.register(TemperatureLog)
class TemperatureLogAdmin(admin.ModelAdmin):
    list_display = ['locker', 'temperature', 'recorded_at', 'is_violation']
    list_filter = ['is_violation']