from django.utils import timezone
from datetime import timedelta
from .models import Locker, TemperatureLog


def check_temperature_violations():
    """
    Check all occupied lockers for temperature violations.
    Rule: If temperature exceeds 41°F for 30+ consecutive minutes,
    mark the order as compromised.
    """

    occupied_lockers = Locker.objects.filter(status='occupied')
    violated_orders = []

    for locker in occupied_lockers:
        thirty_minutes_ago = timezone.now() - timedelta(minutes=30)
        recent_logs = TemperatureLog.objects.filter(
            locker=locker,
            recorded_at__gte=thirty_minutes_ago
        ).order_by('recorded_at')

        if recent_logs.count() < 2:
            continue

        all_above_threshold = all(log.temperature > 41.0 for log in recent_logs)

        if all_above_threshold:
            order = locker.current_order

            if order and order.status not in ['compromised', 'picked_up', 'expired']:
                # Mark order as compromised
                order.status = 'compromised'
                order.save()

                # Mark logs as violations
                recent_logs.update(is_violation=True)

                # Release the locker
                locker.status = 'available'
                locker.current_order = None
                locker.save()

                temperature_readings = [log.temperature for log in recent_logs]

                # Send notifications
                try:
                    from notifications.utils import (
                        send_order_compromised_email_student,
                        send_order_compromised_email_manager,
                        send_compromised_sms,
                    )
                    send_order_compromised_email_student(order)
                    send_order_compromised_email_manager(order, temperature_readings)
                    send_compromised_sms(order)
                except Exception as e:
                    print(f"Notification error: {e}")

                violated_orders.append({
                    'order_id': order.id,
                    'locker_number': locker.locker_number,
                    'student': order.student.username,
                    'temperature_readings': temperature_readings,
                })

    return violated_orders