from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

# Create your views here.
from apps.authentication.models import Appointment, CustomUser

from apps.common.utils import get_day_of_week

from .serializers import (
    AppointmentSerializer,
    CalendarSerializer,
    UpdateAvailabilitySerializer,
)


class AppointmentListView(generics.ListAPIView):
    """
    Returns all active appointments
    """

    queryset = Appointment.objects.filter(appointment_session__gte=timezone.now())
    serializer_class = AppointmentSerializer

    def list(self, request, *args, **kwargs):
        """
        GET verb, to return all active appointments
        """
        queryset = self.get_queryset()
        filterset = self.filter_queryset(queryset)
        serializer = AppointmentSerializer(filterset, many=True)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


class CalendarCreateView(APIView):
    """
    Create availability days endpoint
    """

    def post(self, request):
        if not request.user.role == "Doctor":
            raise serializers.ValidationError(
                detail="You are not allowed to add appointment availability days"
            )
        serializer = UpdateAvailabilitySerializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.data
        response_data["days"] = CalendarSerializer(
            request.user.calendar.all(), many=True
        ).data
        return Response(
            {"success": True, "data": response_data}, status=status.HTTP_201_CREATED
        )


class AppointmentCreateView(APIView):
    """
    Create availability days endpoint
    """

    def post(self, request):
        if not request.user.role == "Patient":
            raise serializers.ValidationError(
                detail="Only patients allowed to book appointment"
            )
        serializer = AppointmentSerializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        doctor = serializer.validated_data["doctor"]
        appointment_session = serializer.validated_data["appointment_session"]
        appointment_day = get_day_of_week(appointment_session.weekday())
        if not doctor.calendar.filter(day=appointment_day).exists():
            raise serializers.ValidationError(
                detail="The doctor you selected is not available on the chosen date"
            )
        else:
            calendar = doctor.calendar.filter(
                day=appointment_day,
                from_time__lte=appointment_session.time(),
                to_time__gte=appointment_session.time(),
            )
            if calendar is None or not calendar.exists():
                raise serializers.ValidationError(
                    detail=f"The doctor selected is unavailable within the selected time frame on {appointment_session}"
                )
        serializer.save(patient=request.user)
        response_data = serializer.data
        return Response(
            {"success": True, "data": response_data}, status=status.HTTP_201_CREATED
        )