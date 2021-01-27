import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from apps.authentication.models import CustomUser, Appointment, Calendar
from apps.common.utils import get_day_of_week


@pytest.fixture(scope="function")
def unauthenticated_client():
    return APIClient()


@pytest.fixture(scope="function")
def test_password():
    return "strong-test-password"


@pytest.fixture(scope="function")
def test_email():
    return "test@test.com"


@pytest.fixture(scope="function")
def create_user(
    db,
    test_password,
    test_email,
):
    def make_user(
        is_doctor=False, is_patient=True, emailPasswordNotSupplied=True, **kwargs
    ):

        if emailPasswordNotSupplied:
            if "password" not in kwargs:
                kwargs["password"] = test_password
            if "email" not in kwargs:
                kwargs["email"] = test_email
        if is_doctor:
            user = CustomUser.objects.create_user(
                first_name="doctorFirstName",
                last_name="doctorLastName",
                role="Doctor",
                **kwargs,
            )
        elif is_patient:
            user = CustomUser.objects.create_user(
                first_name="patientFirstName",
                last_name="patientLastName",
                role="Patient",
                **kwargs,
            )
        user.set_password(kwargs["password"])
        user.save()
        return kwargs["password"], user

    return make_user


@pytest.fixture(scope="function")
def get_token():
    def a_token(user_obj, unhashed_password):
        url = reverse("token_obtain_pair")
        data = {
            "email": user_obj.email,
            "password": unhashed_password,
        }
        client = APIClient()
        res = client.post(url, data=data, format="json")
        access_token = res.json()["data"]["access"]
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        return client

    return a_token


@pytest.fixture(scope="function")
def authenticated_client(db, create_user, get_token):
    def prepare_client(
        is_doctor=False,
        is_patient=True,
        unauthorized_token=False,
        create_new_user=True,
        user=None,
        unhashed_password=None,
    ):
        if unauthorized_token:
            return APIClient()
        if create_new_user or user is None or unhashed_password is None:
            if is_doctor:
                unhashed_password, user = create_user(is_doctor=True)
            elif is_patient:
                unhashed_password, user = create_user(is_patient=True)
            else:
                unhashed_password, user = create_user(is_patient=True)

        return get_token(user, unhashed_password)

    return prepare_client


@pytest.fixture(scope="function")
def login_as_user(db, get_token):
    def prepare_client(user, unhashed_password, unauthorized_token=False):
        if unauthorized_token:
            return APIClient()

        return get_token(user, unhashed_password)

    return prepare_client


@pytest.fixture(scope="function")
def create_appointment(db, create_user):
    _, doctor = create_user(
        emailPasswordNotSupplied=False,
        is_doctor=True,
        password="doctorPassword",
        email="doctorEmail@test.com",
    )
    _, patient = create_user(
        emailPasswordNotSupplied=False,
        is_patient=True,
        password="patientPassword",
        email="patientEmail@test.com",
    )
    return Appointment.objects.create(
        doctor=doctor, patient=patient, appointment_session=timezone.now()
    )


@pytest.fixture(scope="function")
def create_calendar(db):
    thirty_minutes_from_now = timezone.now() + timezone.timedelta(minutes=30)
    calendar = Calendar.objects.create(
        day=get_day_of_week(timezone.now().weekday()),
        from_time=timezone.now().strftime("%H:%M"),
        to_time=thirty_minutes_from_now.strftime("%H:%M"),
    )
    return calendar


@pytest.fixture(scope="function")
def create_doctor_with_avaliabilty_date(db, create_user, create_calendar):
    _, doctor = create_user(
        emailPasswordNotSupplied=False,
        is_doctor=True,
        password="doctorPassword",
        email="doctorEmail@test.com",
    )
    doctor.calendar.add(create_calendar)

    return doctor
