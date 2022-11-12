from django.shortcuts import redirect
from rest_framework import views, generics, status
from .models import Notification, NotificationType
from authentication.models import MyUser
from rest_framework import permissions
from .serializers import NotificationSerializer, NotificationTypeSerializer
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class NotificationListApiView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class CreateNotificationApiView(generics.CreateAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class EditDeleteNotificationApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class CreateNotificationTypeApiView(generics.CreateAPIView):
    serializer_class = NotificationTypeSerializer
    queryset = NotificationType.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_queryset(self):
        return NotificationType.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        new_type = MyUser.objects.get(id=self.request.user.pk).notification_type.create(name_type=request.data['name_type'], color=request.data['color'])
        new_type.save()
        return redirect('notification_list_api_view')
