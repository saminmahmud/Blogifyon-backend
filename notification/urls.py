# blog/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import NotificationView

router = DefaultRouter()

router.register('', NotificationView) 

urlpatterns = [
    path('', include(router.urls)),
    # path('', NotificationListView.as_view(), name='notificationlist'),NotificationListView,
    # path('readnotification/<int:pk>/', MarkNotificationReadView.as_view(), name='readnotification'),
]