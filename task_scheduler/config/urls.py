"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from notifications.views import HomeView
from rest_framework import routers
from notifications.api_view import NotificationListApiView, CreateNotificationApiView, EditDeleteNotificationApiView, CreateNotificationTypeApiView
from authentication.api_view import RegisterApiView, LoginApiView, logoutApiView, UserProfileApiView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomeView.as_view(), name="home"),

    #api notifications
    path('api/notifications/', NotificationListApiView.as_view(), name='notification_list_api_view'),
    path('api/notifications/create/', CreateNotificationApiView.as_view(), name='create_notification_api_view'),
    path('api/notifications/edit/<int:pk>/', EditDeleteNotificationApiView.as_view(), name='create_notification_api_view'),
    path('api/notifications/create_new_type/', CreateNotificationTypeApiView.as_view(), name='create_notificationtype_api_view'),


    #api auth
    path('api/auth/registration/', RegisterApiView.as_view(), name='user_registration_api'),
    path('api/auth/login/', LoginApiView.as_view(), name='user_login_api'),
    path('api/auth/logout/', logoutApiView, name='user_logout_api'),
    path('api/auth/profile/', UserProfileApiView.as_view(), name='user_profile'),


    # Notifications
    path('notifications/', include('notifications.urls')),

    # Auth
    path('auth/', include('authentication.urls'))

]
