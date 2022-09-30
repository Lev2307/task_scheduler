from django.urls import path
from .views import NotificationListView, NotificationCreateView

urlpatterns = [
    path('read/', NotificationListView.as_view(), name="notification_list"),
    path('create/', NotificationCreateView.as_view(), name="create_notification"),
]