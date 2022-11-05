from .models import MyUser
from django.contrib.auth import login
from rest_framework import views, permissions, status, generics
from rest_framework.response import Response
from .serializers import MyUserRegisterSerializer, MyUserLoginSerializer

class RegisterApiView(generics.CreateAPIView):
    serializer_class = MyUserRegisterSerializer
    queryset = MyUser.objects.all()
    permission_classes = [permissions.AllowAny]

class LoginApiView(views.APIView):
    serializer_class = MyUserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = MyUserLoginSerializer(data=self.request.data,
            context={'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)