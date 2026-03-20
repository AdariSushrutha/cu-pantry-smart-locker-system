from django.urls import path
from .views import LockerListView, LockerAssignView, TemperatureLogListView

urlpatterns = [
    path('', LockerListView.as_view(), name='locker-list'),
    path('assign/', LockerAssignView.as_view(), name='locker-assign'),
    path('temperature-logs/', TemperatureLogListView.as_view(), name='temperature-logs'),
]