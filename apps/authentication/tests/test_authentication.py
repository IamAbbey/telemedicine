import pytest
from django.urls import reverse
from rest_framework import status

from core.tests.conftest import *


@pytest.mark.django_db
@pytest.mark.xfail
def test_unauthorized_request(unauthenticated_client):
    url = reverse("token_obtain_pair")
    response = unauthenticated_client.post(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_all_user(authenticated_client):
    url = reverse("users_list")
    response = authenticated_client().get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"]
    assert len(response.data["data"]) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "email, password, role, first_name, last_name, status_code",
    [
        pytest.param(None, None, None, None, None, 400, marks=pytest.mark.bad_request),
        pytest.param(
            None,
            "strong_pass",
            None,
            None,
            None,
            400,
            marks=pytest.mark.bad_request,
        ),
        pytest.param(
            "some@magic.email",
            None,
            None,
            None,
            None,
            400,
            marks=[pytest.mark.bad_request],
        ),
        pytest.param(
            "user@example.com",
            "strong_pass",
            None,
            None,
            None,
            400,
            marks=[pytest.mark.bad_request],
        ),
        pytest.param(
            "user@example.com",
            "strong_pass",
            "Doctor",
            None,
            None,
            400,
            marks=[pytest.mark.bad_request],
        ),
        pytest.param(
            "user@example.com",
            "strong_pass",
            "Patient",
            None,
            None,
            400,
            marks=[pytest.mark.bad_request],
        ),
        pytest.param(
            "user@example.com",
            "strong_pass",
            "Patient",
            "testFirstName",
            None,
            400,
            marks=[pytest.mark.bad_request],
        ),
        pytest.param(
            "user@example.com",
            "strong_pass",
            "Patient",
            "testFirstName",
            "testLastName",
            201,
            marks=pytest.mark.success_request,
        ),
    ],
)
def test_create_user(
    email, password, role, first_name, last_name, status_code, unauthenticated_client
):
    url = reverse("create_user")
    data = {
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "role": role,
        "email": email,
    }
    response = unauthenticated_client.post(url, data, format="json")
    print(response.data)
    assert response.status_code == status_code


@pytest.mark.xfail
@pytest.mark.django_db
def test_get_user_details_not_authorized(unauthenticated_client, create_user):
    password, user = create_user(is_doctor=True)
    url = reverse("user_details", kwargs={"user_id": user.pk})
    response = unauthenticated_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert not response.data["success"]


@pytest.mark.django_db
def test_get_user_details(authenticated_client, create_user):
    password, user = create_user(is_patient=True)
    url = reverse("user_details", kwargs={"user_id": user.pk})
    response = authenticated_client(create_new_user=False, user=user, unhashed_password=password).get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"]
    assert response.data["data"]["email"] == user.email
    assert not response.data["data"]["is_staff"]

@pytest.mark.django_db
@pytest.mark.parametrize(
    "unauthorized, success_status, status_code",
    [
        pytest.param(
            True, False, status.HTTP_401_UNAUTHORIZED, marks=[pytest.mark.bad_request]
        ),
        pytest.param(
            False, True, status.HTTP_200_OK, marks=[pytest.mark.success_request]
        ),
    ],
)
def test_update_user(
    unauthorized,
    success_status,
    status_code,
    create_user,
    login_as_user,
):
    _, user = create_user(password="test")
    assert user.first_name == "patientFirstName"

    url = reverse("user_details", kwargs={"user_id": user.pk})
    data = {"first_name": "test_user"}
    resp = login_as_user(
        user=user, unhashed_password="test", unauthorized_token=unauthorized
    ).put(url, data=data)
    assert resp.status_code == status_code
    assert resp.data["success"] == success_status
    if not unauthorized:
        assert resp.data["data"]["first_name"] == "test_user"