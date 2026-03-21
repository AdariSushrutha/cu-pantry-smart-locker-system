from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from .utils import assign_qr_and_pin
from notifications.utils import (
    send_order_ready_email,
    send_order_ready_sms,
    send_order_compromised_email_student,
    send_compromised_sms,
)


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Students only see their own orders
        if not user.is_staff:
            return Order.objects.filter(student=user).order_by('-created_at')

        # Staff see all orders
        return Order.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save()


class OrderDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Students can only see their own orders
        if not user.is_staff:
            return Order.objects.filter(student=user)

        # Staff can see all orders
        return Order.objects.all()

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        new_status = request.data.get('status')

        # Only staff can update order status
        if not request.user.is_staff:
            return Response(
                {'error': 'You do not have permission to update order status.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Validate status transition
        valid_transitions = {
            'submitted': ['approved'],
            'approved': ['locker_assigned'],
            'locker_assigned': ['ready'],
            'ready': ['picked_up', 'expired', 'compromised'],
        }

        current_status = order.status
        allowed = valid_transitions.get(current_status, [])

        if new_status not in allowed:
            return Response(
                {'error': f'Cannot transition from {current_status} to {new_status}.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update status
        order.status = new_status
        order.save()

        # Trigger notifications based on new status
        if new_status == 'ready':
            # Generate QR code and PIN
            assign_qr_and_pin(order)

            # Send notifications
            try:
                send_order_ready_email(order)
                send_order_ready_sms(order)
            except Exception as e:
                print(f"Notification error: {e}")

        elif new_status == 'compromised':
            # Notify student
            try:
                send_order_compromised_email_student(order)
                send_compromised_sms(order)
            except Exception as e:
                print(f"Notification error: {e}")

        return Response(OrderSerializer(order).data)