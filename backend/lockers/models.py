from django.db import models

# Create your models here.
from django.db import models

class Locker(models.Model):

    TEMPERATURE_CHOICES = [
        ('frozen', 'Frozen'),
        ('refrigerated', 'Refrigerated'),
        ('ambient', 'Ambient'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Maintenance'),
    ]

    locker_number = models.CharField(max_length=20, unique=True)
    temperature_type = models.CharField(max_length=20, choices=TEMPERATURE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    bell_howell_id = models.CharField(max_length=100, null=True, blank=True)
    current_order = models.OneToOneField(
        'orders.Order',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_locker'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Locker {self.locker_number} ({self.temperature_type})"


class TemperatureLog(models.Model):
    locker = models.ForeignKey(Locker, on_delete=models.CASCADE, related_name='temperature_logs')
    temperature = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)
    is_violation = models.BooleanField(default=False)

    def __str__(self):
        return f"Locker {self.locker.locker_number} - {self.temperature}°F at {self.recorded_at}"