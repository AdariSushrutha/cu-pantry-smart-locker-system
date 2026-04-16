from django.urls import path
from .views import (
    InventoryListCreateView,
    InventoryDetailView,
    BarcodeLookupView,
    BarcodeUpdateInventoryView
)

urlpatterns = [
    path('', InventoryListCreateView.as_view(), name='inventory-list-create'),
    path('<int:pk>/', InventoryDetailView.as_view(), name='inventory-detail'),
    path('barcode/<str:barcode>/', BarcodeLookupView.as_view(), name='barcode-lookup'),
    path('barcode/scan/', BarcodeUpdateInventoryView.as_view(), name='barcode-scan'),
]