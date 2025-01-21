
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from django.contrib.auth import get_user_model
User = get_user_model()

class NotificationView(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    filter_backends = (SearchFilter,)
    search_fields = ['user__user__id']
    authentication_classes = []
    permission_classes = []


# class MarkNotificationReadView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, pk):
#         try:
#             notification = Notification.objects.get(pk=pk, user=request.user)
#         except Notification.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         notification.is_read = True
#         notification.save()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
# class MarkNotificationReadView(APIView):
#     def post(self, request, pk):
#         try:
#             notification = Notification.objects.get(pk=pk, user=request.user)
#         except Notification.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         notification.is_read = True
#         notification.save()
#         return Response(status=status.HTTP_204_NO_CONTENT)
