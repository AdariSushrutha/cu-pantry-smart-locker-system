from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'service_insights_id', 'phone_number', 'created_at']
    search_fields = ['user__username', 'service_insights_id']