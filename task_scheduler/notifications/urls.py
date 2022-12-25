from django.urls import path
from .views import (
        NotificationListView,
        NotificationSingleCreateView,
        NotificationSingleEditView, 
        NotificationSingleDeleteView,
        NotificationSingleDetailView, 
        AddNotificationTypeView, 
        PeriodicalNotificationCreateView,
        NotificationPeriodicDetailView,
    )

urlpatterns = [
    path('read/', NotificationListView.as_view(), name="notification_list"),
    path('create/', NotificationSingleCreateView.as_view(), name="create_notification"),
    path('edit/<int:pk>/', NotificationSingleEditView.as_view(), name="edit_notification"),
    path('delete/<int:pk>/', NotificationSingleDeleteView.as_view(), name="delete_notification"),
    path('single/<int:pk>/', NotificationSingleDetailView.as_view(), name="detail_single_notification"),
    path('periodic/<int:pk>/', NotificationPeriodicDetailView.as_view(), name="detail_periodic_notification"),
    path('add_notification_type/', AddNotificationTypeView.as_view(), name="add_notification_type"),
    path('create_periodical_notification/', PeriodicalNotificationCreateView.as_view(), name="create_periodical_notification")
]