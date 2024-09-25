from django.urls import path
from users.api.views import (RegisterView, LoginView, ChangePasswordView,
                             UserProfileView, UpdateProfileView, UserDetailView,
                             GetUserByNameView, UserListAll)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("update-profile/", UpdateProfileView.as_view(), name="update-profile"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("filter-by-name/", GetUserByNameView.as_view(), name="filter-users-by-name"),
    path("all/", UserListAll.as_view(), name="user-list-all"),
]