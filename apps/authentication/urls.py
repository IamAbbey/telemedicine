"""telemedicine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserListView,
    CustomTokenObtainPairView,
    UserCreateView,
    UserDetailView,
)

urlpatterns = [
    path("auth/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("all/", UserListView.as_view(), name="users_list"),
    path("save/", UserCreateView.as_view(), name="create_user"),
    path("<int:user_id>/", UserDetailView.as_view(), name="user_details"),
]
