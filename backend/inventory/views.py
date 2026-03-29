from rest_framework import generics, permissions
from .models import InventoryItem
from .serializers import InventoryItemSerializer
from authentication.permissions import IsManager


class InventoryListCreateView(generics.ListCreateAPIView):
    serializer_class = InventoryItemSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            # Everyone logged in can view inventory
            return [permissions.IsAuthenticated()]
        # Only managers can add items
        return [IsManager()]

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
    queryset = InventoryItem.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            # Everyone logged in can view individual items
            return [permissions.IsAuthenticated()]
        # Only managers can update or delete items
        return [IsManager()]