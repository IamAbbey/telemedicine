from django.db import models
from django.contrib.auth.models import AbstractUser

from .manager import CustomUserManager

# Create your models here.

ROLES = (("Doctor", "Doctor"), ("Patient", "Patient"))

DAYS_OF_WEEK = (
    ("Monday", "Monday"),
    ("Tuesday", "Tuesday"),
    ("Wednesday", "Wednesday"),
    ("Thursday", "Thursday"),
    ("Friday", "Friday"),
    ("Saturday", "Saturday"),
    ("Sunday", "Sunday"),
)


class CustomUser(AbstractUser):
    role = models.CharField(max_length=50, choices=ROLES)
    calendar = models.ManyToManyField("Calendar")
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Appointment(models.Model):

    doctor = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="doctor"
    )
    patient = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="patient"
    )
    appointment_session = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"

    def __str__(self):
        return self.doctor.first_name


class Calendar(models.Model):

    day = models.CharField(max_length=50, choices=DAYS_OF_WEEK)
    from_time = models.TimeField()
    to_time = models.TimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Calendar"
        verbose_name_plural = "Calendars"

    def __str__(self):
        return f"{self.day} : {self.from_time} - {self.to_time}"
