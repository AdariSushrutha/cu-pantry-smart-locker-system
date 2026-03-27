from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):

    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('locker_assigned', 'Locker Assigned'),
        ('ready', 'Ready'),
        ('picked_up', 'Picked Up'),
        ('expired', 'Expired'),
        ('compromised', 'Compromised'),
    ]

    TEMPERATURE_CHOICES = [
        ('frozen', 'Frozen'),
        ('refrigerated', 'Refrigerated'),
        ('ambient', 'Ambient'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    temperature_category = models.CharField(
        max_length=20,
        choices=TEMPERATURE_CHOICES,
        null=True,
        blank=True
    )
    requires_lower_locker = models.BooleanField(default=False)
    week_number = models.IntegerField()
    year = models.IntegerField()
    pickup_date = models.DateField(null=True, blank=True)
    pickup_deadline = models.DateTimeField(null=True, blank=True)
    qr_token = models.CharField(max_length=255, null=True, blank=True)
    pin_code = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'week_number', 'year')

    def __str__(self):
        return f"Order #{self.id} - {self.student.username} - {self.status}"