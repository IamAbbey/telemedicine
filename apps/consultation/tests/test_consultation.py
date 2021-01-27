import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from core.tests.conftest import *


@pytest.mark.django_db
def test_get_all_appointments(authenticated_client, create_appointment):
    url = reverse("appointment_list")
    response = authenticated_client().get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"]
    assert len(response.data["data"]) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "days, is_doctor, status_code",
    [
        pytest.param(None, None, 400, marks=pytest.mark.bad_request),
        pytest.param(
            None,
            False,
            400,
            marks=pytest.mark.bad_request,
        ),
        pytest.param(
            None,
            True,
            400,
            marks=pytest.mark.bad_request,
        ),
        pytest.param(
            [
                {"day": "Monday", "from_time": "12:20", "to_time": "15:10"},
                {"day": "Wednesday", "from_time": "13:20", "to_time": "16:10"},
            ],
            False,
            400,
            marks=[pytest.mark.bad_request],
        ),
        pytest.param(
            [
                {"day": "Monday", "from_time": "12:20", "to_time": "15:10"},
                {"day": "Wednesday", "from_time": "13:20", "to_time": "16:10"},
            ],
            True,
            201,
            marks=pytest.mark.success_request,
        ),
    ],
)
def test_add_availability(days, is_doctor, status_code, authenticated_client, db):
    url = reverse("add_availability")
    data = {
        "days": days,
    }
    response = authenticated_client(is_doctor=is_doctor).post(url, data, format="json")
    print(response.data)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "doctor_id_valid, appointment_session, status_code",
    [
        pytest.param(None, None, 400, marks=pytest.mark.bad_request),
        pytest.param(
            False,
            None,
            400,
            marks=pytest.mark.bad_request,
        ),
        pytest.param(
            True,
            None,
            400,
            marks=pytest.mark.bad_request,
        ),
        pytest.param(
            True,
            "2019-01-27T16:13:37.861783+01:00",
            400,
            marks=pytest.mark.bad_request,
        ),
        pytest.param(
            True,
            timezone.now() - timezone.timedelta(hours=1),
            201,
            marks=pytest.mark.success_request,
        ),
    ],
)
def test_add_appointment(
    doctor_id_valid,
    appointment_session,
    status_code,
    authenticated_client,
    db,
    create_doctor_with_avaliabilty_date,
):
    url = reverse("add_appointment")
    doctor = create_doctor_with_avaliabilty_date
    data = {
        "doctor": doctor.id if doctor_id_valid else 20,
        "appointment_session": appointment_session,
    }
    response = authenticated_client().post(url, data, format="json")
    assert response.status_code == status_code


def test_add_appointment_is_doctor(
    authenticated_client,
    db,
    create_doctor_with_avaliabilty_date,
):
    url = reverse("add_appointment")
    doctor = create_doctor_with_avaliabilty_date
    data = {
        "doctor": doctor.id,
        "appointment_session": timezone.now() - timezone.timedelta(hours=1),
    }
    response = authenticated_client(is_doctor=True).post(url, data, format="json")
    assert response.status_code == 400


def test_add_appointment_invalid_appointment_session(
    authenticated_client,
    db,
    create_doctor_with_avaliabilty_date,
):
    url = reverse("add_appointment")
    doctor = create_doctor_with_avaliabilty_date
    data = {
        "doctor": doctor.id,
        "appointment_session": timezone.now() - timezone.timedelta(hours=10),
    }
    response = authenticated_client(is_doctor=True).post(url, data, format="json")
    assert response.status_code == 400
