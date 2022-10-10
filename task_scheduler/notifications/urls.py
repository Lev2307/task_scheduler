from django.urls import path
from .views import NotificationListView, NotificationCreateView, NotificationEditView, NotificationDeleteView, UserNotificationCategoriesView

urlpatterns = [
    path('read/', NotificationListView.as_view(), name="notification_list"),
    path('create/', NotificationCreateView.as_view(), name="create_notification"),
    path('edit/<int:pk>/', NotificationEditView.as_view(), name="edit_notification"),
    path('delete/<int:pk>/', NotificationDeleteView.as_view(), name="delete_notification"),
    path('new_notification_category/', UserNotificationCategoriesView.as_view(), name="add_new_notification_category")
]