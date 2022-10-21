from django.urls import path
from .views import RegisterView, LoginView, LogoutView, UserProfileView

urlpatterns = [
    # Auth
    path('registration/', RegisterView.as_view(), name="registration"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('profile/', UserProfileView.as_view(), name="profile"),
]