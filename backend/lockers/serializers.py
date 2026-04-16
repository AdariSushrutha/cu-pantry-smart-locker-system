from rest_framework import serializers
from .models import Locker, TemperatureLog
from orders.models import Order


class LockerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locker
        fields = [
            'id',
            'locker_number',
            'temperature_type',
            'status',
            'bell_howell_id',
            'current_order',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LockerAssignSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    locker_id = serializers.IntegerField()

    def validate(self, data):
        # Check order exists
        try:
            order = Order.objects.get(id=data['order_id'])
        except Order.DoesNotExist:
            raise serializers.ValidationError("Order not found.")

        # Check locker exists
        try:
            locker = Locker.objects.get(id=data['locker_id'])
        except Locker.DoesNotExist:
            raise serializers.ValidationError("Locker not found.")

        # Check order status is approved
        if order.status != 'approved':
            raise serializers.ValidationError(
                "Order must be approved before assigning a locker."
            )

        # Check locker is available
        if locker.status != 'available':
            raise serializers.ValidationError(
                f"Locker {locker.locker_number} is not available."
            )

        data['order'] = order
        data['locker'] = locker
        return data


class TemperatureLogSerializer(serializers.ModelSerializer):
    locker_number = serializers.CharField(source='locker.locker_number', read_only=True)

    class Meta:
        model = TemperatureLog
        fields = [
            'id',
            'locker_number',
            'temperature',
            'recorded_at',
            'is_violation',
        ]
        read_only_fields = ['id', 'recorded_at', 'is_violation']