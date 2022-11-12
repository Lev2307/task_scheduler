from django.shortcuts import redirect
from .models import MyUser
from django.contrib.auth import login, logout
from rest_framework import views, permissions, status, generics, mixins
from rest_framework.response import Response
from notifications.models import NotificationType

from rest_framework.decorators import api_view
from .serializers import MyUserRegisterSerializer, MyUserLoginSerializer, UserProfileSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class RegisterApiView(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = MyUserRegisterSerializer
    queryset = MyUser.objects.all()
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return Response('registration page')

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class LoginApiView(generics.GenericAPIView):
    serializer_class = MyUserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return Response('login page')

    def post(self, request, format=None):
        serializer = MyUserLoginSerializer(data=self.request.data,
            context={'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)

@api_view(['GET', 'POST'])
def logoutApiView(request):
    logout(request)
    return redirect('/')

class UserProfileApiView(generics.RetrieveAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserProfileSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_queryset(self):
        return self.queryset.filter(pk=self.request.user.pk)
    
    def get(self, request, *args, **kwargs):
        user_profile = MyUser.objects.get(username=request.user)
        serializer = self.serializer_class(user_profile)
        all_notification_types_data = []
        for notification_type_name in MyUser.objects.get(username=request.user).notification_type.all():
            notification_type_name =  MyUser.objects.get(username=request.user).notification_type.get(name_type=str(notification_type_name))
            all_notification_types_data.append(str(notification_type_name))
        return Response({"data": serializer.data, "notification_types": all_notification_types_data}, status=status.HTTP_202_ACCEPTED)

    