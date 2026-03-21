import qrcode
import io
import random
import string
from django.utils import timezone
from datetime import timedelta


def generate_pin():
    """Generate a random 6 digit PIN"""
    return ''.join(random.choices(string.digits, k=6))


def generate_qr_token():
    """Generate a unique token for the QR code"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))


def generate_qr_code_image(order):
    """
    Generate a QR code image for the order.
    The QR code contains a secure URL with the order token.
    """
    # The QR code will encode a secure pickup URL
    qr_data = f"https://pantry.clarkson.edu/pickup/{order.qr_token}"

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Create image
    img = qr.make_image(fill_color="black", back_color="white")

    # Save to bytes buffer
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    return buffer


def assign_qr_and_pin(order):
    """
    Generate and assign QR token and PIN to an order.
    Sets the pickup deadline to 48 hours from now.
    """
    order.qr_token = generate_qr_token()
    order.pin_code = generate_pin()
    order.pickup_deadline = timezone.now() + timedelta(hours=48)
    order.save()
    return order