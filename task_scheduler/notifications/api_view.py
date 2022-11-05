from rest_framework import viewsets
from .models import Notification
from rest_framework import permissions
from .serializers import NotificationSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]