from rest_framework import serializers

from apps.authentication.models import Appointment, Calendar
from apps.authentication.serializers import UserSerializer


class AppointmentSerializer(serializers.ModelSerializer):

    doctor_obj = UserSerializer(source="doctor", read_only=True)
    patient_obj = UserSerializer(source="patient", read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "doctor",
            "appointment_session",
            "doctor_obj",
            "patient_obj",
        ]

    read_only_fields = (
        "id",
        "patient",
        "created_date",
        "updated_date",
    )

    def create(self, validated_data):
        appointment = Appointment.objects.create(**validated_data)
        return appointment


class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = "__all__"

    read_only_fields = (
        "id",
        "created_date",
        "updated_date",
    )


class UpdateAvailabilitySerializer(serializers.Serializer):
    days = serializers.ListField(child=serializers.DictField(), max_length=7)

    def create(self, validated_data):
        user = self.context["user"]
        data = validated_data.get("days")
        for config in data:
            calendar_s = CalendarSerializer(data=config)
            calendar_s.is_valid(raise_exception=True)
            day = calendar_s.validated_data["day"]
            if user.calendar.filter(day=day).exists():
                calendar = user.calendar.filter(day=day).first()
                calendar.from_time = calendar_s.validated_data["from_time"]
                calendar.to_time = calendar_s.validated_data["to_time"]
                calendar.save()
            else:
                obj = calendar_s.save()
                user.calendar.add(obj)

        return {"days": []}
