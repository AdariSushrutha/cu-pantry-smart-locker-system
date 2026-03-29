from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import InventoryItem
from .serializers import InventoryItemSerializer


class IsStaffOrReadOnly(permissions.BasePermission):
    """Students can view inventory, only staff can edit"""
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user.is_authenticated
        return request.user.is_staff


class InventoryListCreateView(generics.ListCreateAPIView):
    serializer_class = InventoryItemSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        queryset = InventoryItem.objects.all().order_by('name')

        # Filter by availability
        is_available = self.request.query_params.get('available')
        if is_available:
            queryset = queryset.filter(is_available=True)

        # Filter by temperature category
        temp_category = self.request.query_params.get('temperature')
        if temp_category:
            queryset = queryset.filter(temperature_category=temp_category)

        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)

        return queryset


class InventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InventoryItemSerializer
    permission_classes = [IsStaffOrReadOnly]
    queryset = InventoryItem.objects.all()