from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Locker, TemperatureLog
from .serializers import LockerSerializer, LockerAssignSerializer, TemperatureLogSerializer


class LockerListView(generics.ListAPIView):
    serializer_class = LockerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only staff can view all lockers
        if self.request.user.is_staff:
            return Locker.objects.all().order_by('locker_number')
        return Locker.objects.none()


class LockerAssignView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Only staff can assign lockers
        if not request.user.is_staff:
            return Response(
                {'error': 'You do not have permission to assign lockers.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = LockerAssignSerializer(data=request.data)

        if serializer.is_valid():
            order = serializer.validated_data['order']
            locker = serializer.validated_data['locker']

            # Assign locker to order
            locker.status = 'occupied'
            locker.current_order = order
            locker.save()

            # Update order status
            order.status = 'locker_assigned'
            order.save()

            return Response({
                'message': f'Locker {locker.locker_number} assigned to order #{order.id}',
                'order_id': order.id,
                'locker_number': locker.locker_number,
                'order_status': order.status,
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemperatureLogListView(generics.ListCreateAPIView):
    serializer_class = TemperatureLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return TemperatureLog.objects.all().order_by('-recorded_at')
        return TemperatureLog.objects.none()

    def perform_create(self, serializer):
        # Check for temperature violation (over 41°F)
        temperature = serializer.validated_data.get('temperature')
        is_violation = temperature > 41.0
        serializer.save(is_violation=is_violation)