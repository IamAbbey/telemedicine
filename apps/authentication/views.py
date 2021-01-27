from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from apps.common.permissions import (
    IsAdminOrReadOnly,
    IsOwnerOrReadOnly,
    IsSuperUser,
    IsUserOwnerOrReadOnly,
)
# Create your views here.


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Authentication endpoint to get access tokens
    """

    def post(self, request, *args, **kwargs):
        payload = request.data
        serializer = CustomTokenObtainPairSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        response_payload = serializer.validated_data
        return Response(
            {"success": True, "data": response_payload}, status=status.HTTP_200_OK
        )


class UserListView(generics.ListAPIView):
    """
    Returns all active users
    """

    queryset = CustomUser.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        """
        GET verb, to return all active users
        """
        queryset = self.get_queryset()
        filterset = self.filter_queryset(queryset)
        serializer = UserSerializer(filterset, many=True)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


class UserCreateView(generics.CreateAPIView):
    """
    Create user endpoint
    """

    serializer_class = UserSerializer
    permission_classes = []

    def perform_create(self, serializer):
        user = serializer.save()
        self.kwargs["user"] = user

    def create(self, request, *args, **kwargs):
        response = super().create(request)
        refresh = RefreshToken.for_user(self.kwargs["user"])
        response_data = response.data
        response_data["access"] = str(refresh.access_token)
        return Response(
            {"success": True, "data": response_data}, status=status.HTTP_201_CREATED
        )


class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    Enpoint to get a particular user details, update and delete user's record
    Only the admins can perform non SAFE METHODS
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserOwnerOrReadOnly]
    lookup_url_kwarg = "user_id"
    lookup_field = "id"
    queryset = CustomUser.objects.all()

    def get(self, request, *args, **kwargs):
        response = super().get(request)
        return Response(
            {"success": True, "data": response.data}, status=status.HTTP_200_OK
        )

    def put(self, request, *args, **kwargs):
        response = super().patch(request)
        return Response(
            {"success": True, "data": response.data}, status=status.HTTP_200_OK
        )