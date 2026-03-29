from rest_framework import serializers
from .models import Order
import datetime


class OrderSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)
    pickup_date = serializers.DateField(required=False, allow_null=True)
    pickup_deadline = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'student_username',
            'temperature_category',
            'status',
            'week_number',
            'year',
            'pickup_date',
            'pickup_deadline',
            'qr_token',
            'pin_code',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'status',
            'week_number',
            'year',
            'qr_token',
            'pin_code',
            'created_at',
            'updated_at',
        ]

    def validate(self, data):
        request = self.context.get('request')
        student = request.user
        items = request.data.get('items', [])

        # Get current week and year
        today = datetime.date.today()
        week_number = today.isocalendar()[1]
        year = today.year

        # Check if student already ordered this week
        existing_order = Order.objects.filter(
            student=student,
            week_number=week_number,
            year=year
        ).exists()

        if existing_order:
            raise serializers.ValidationError(
                "You have already placed your locker order for this week. "
                "You may place a new order starting Monday."
            )
        
        # Enforce 5-10 item limit
        if len(items) < 5 or len(items) > 10:
            raise serializers.ValidationError(
                "You must select between 5 and 10 items per order."
        )

        # Inject week and year into data
        data['week_number'] = week_number
        data['year'] = year
        data['student'] = student

        return data