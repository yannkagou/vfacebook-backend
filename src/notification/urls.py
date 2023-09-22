from django.urls import path
from . import api

urlpatterns = [
    path('', api.notifications, name='notifications'),
    path('allnotifs/', api.allnotifications, name='notifications'),
    path('read/<int:id>/', api.read_notification, name='read_notifications'),
]
