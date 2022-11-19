from django.shortcuts import redirect
from rest_framework import mixins, generics, status
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

class CreateNotificationApiView(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get(self, request, *args, **kwargs):
        return Response('Create your notification ;>')

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DetailNotificationApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class CreateNotificationTypeApiView(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = NotificationTypeSerializer
    queryset = NotificationType.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get(self, request, *args, **kwargs):
        return Response("create your notification type ;>")

    def get_queryset(self):
        return NotificationType.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)