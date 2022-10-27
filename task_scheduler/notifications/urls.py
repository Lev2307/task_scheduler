from django.urls import path
from .views import NotificationListView, NotificationCreateView, NotificationEditView, NotificationDeleteView, AddNotificationTypeView

urlpatterns = [
    path('read/', NotificationListView.as_view(), name="notification_list"),
    path('create/', NotificationCreateView.as_view(), name="create_notification"),
    path('edit/<int:pk>/', NotificationEditView.as_view(), name="edit_notification"),
    path('delete/<int:pk>/', NotificationDeleteView.as_view(), name="delete_notification"),
    path('add_notification_type/', AddNotificationTypeView.as_view(), name="add_notification_type"),
    path('add_notification_type/', AddNotificationTypeView.as_view(), name="add_notification_type"),
]