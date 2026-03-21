from django.core.mail import EmailMessage
from django.conf import settings
from orders.utils import generate_qr_code_image


def send_order_ready_email(order):
    """Send email to student when order is ready for pickup"""
    subject = 'Your CU Pantry Order is Ready for Pickup!'

    message = f"""
Hi {order.student.first_name or order.student.username},

Your pantry order is ready for pickup!

Order Details:
- Order ID: #{order.id}
- Locker Number: {order.assigned_locker.locker_number}
- Pickup Date: {order.pickup_date}
- Pickup Deadline: {order.pickup_deadline}
- PIN Code: {order.pin_code}

A QR code is attached to this email. You can use either the QR code 
or your PIN to access your locker.

Important: Your order must be picked up by {order.pickup_deadline}.
After this time, your order will expire and the locker will be released.

If you have any issues, please contact the pantry staff.

CU Smart Pantry Team
"""

    # Generate QR code image
    qr_buffer = generate_qr_code_image(order)

    # Create email with attachment
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[order.student.email],
    )

    # Attach QR code image
    email.attach(
        f'order_{order.id}_qr.png',
        qr_buffer.read(),
        'image/png'
    )

    email.send(fail_silently=False)


def send_order_compromised_email_student(order):
    """Send email to student when order is compromised"""
    subject = 'Important: Your CU Pantry Order Has Been Cancelled'

    message = f"""
Hi {order.student.first_name or order.student.username},

We regret to inform you that your pantry order #{order.id} has been 
cancelled due to a temperature safety issue with the locker.

Your food safety is our top priority. The items in your order may have 
been compromised due to a temperature violation in the locker.

You are eligible to place a new order. Please log in to place a new request.

We apologize for the inconvenience.

CU Smart Pantry Team
"""

    from django.core.mail import send_mail
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[order.student.email],
        fail_silently=False,
    )


def send_order_compromised_email_manager(order, temperature_readings):
    """Send email to manager when order is compromised"""
    subject = f'ALERT: Temperature Violation - Locker {order.assigned_locker.locker_number}'

    message = f"""
TEMPERATURE VIOLATION ALERT

Order #{order.id} has been marked as compromised due to a temperature violation.

Details:
- Locker Number: {order.assigned_locker.locker_number}
- Student: {order.student.username}
- Temperature Readings: {temperature_readings}
- Order Status: {order.status}

The locker has been released and the student has been notified.

Please inspect the locker and take appropriate action.

CU Smart Pantry System
"""

    from django.core.mail import send_mail
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.MANAGER_EMAIL],
        fail_silently=False,
    )


def send_order_ready_sms(order):
    """Send SMS to student when order is ready for pickup"""
    message = (
        f"CU Pantry: Your order is ready! "
        f"Locker: {order.assigned_locker.locker_number}. "
        f"Pickup by: {order.pickup_date}. "
        f"PIN: {order.pin_code}"
    )

    # TODO: Replace with actual SMS gateway when Clarkson provides credentials
    print(f"SMS to {order.student.username}: {message}")


def send_compromised_sms(order):
    """Send SMS to student when order is compromised"""
    message = (
        f"CU Pantry: Your order #{order.id} has been cancelled "
        f"due to a temperature issue. Please log in to place a new order."
    )

    # TODO: Replace with actual SMS gateway when Clarkson provides credentials
    print(f"SMS to {order.student.username}: {message}")