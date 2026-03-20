from django.utils import timezone
from datetime import timedelta
from .models import Locker, TemperatureLog


def check_temperature_violations():
    """
    Check all occupied lockers for temperature violations.
    Rule: If temperature exceeds 41°F for 30+ consecutive minutes,
    mark the order as compromised.
    """

    # Get all occupied lockers
    occupied_lockers = Locker.objects.filter(status='occupied')

    violated_orders = []

    for locker in occupied_lockers:
        # Get temperature logs from the last 30 minutes
        thirty_minutes_ago = timezone.now() - timedelta(minutes=30)
        recent_logs = TemperatureLog.objects.filter(
            locker=locker,
            recorded_at__gte=thirty_minutes_ago
        ).order_by('recorded_at')

        # Need at least 2 readings to detect a violation
        if recent_logs.count() < 2:
            continue

        # Check if ALL recent readings are above 41°F
        all_above_threshold = all(log.temperature > 41.0 for log in recent_logs)

        if all_above_threshold:
            order = locker.current_order

            if order and order.status not in ['compromised', 'picked_up', 'expired']:
                # Mark order as compromised
                order.status = 'compromised'
                order.save()

                # Mark all recent logs as violations
                recent_logs.update(is_violation=True)

                # Release the locker
                locker.status = 'available'
                locker.current_order = None
                locker.save()

                violated_orders.append({
                    'order_id': order.id,
                    'locker_number': locker.locker_number,
                    'student': order.student.username,
                    'temperature_readings': [log.temperature for log in recent_logs],
                })

    return violated_orders