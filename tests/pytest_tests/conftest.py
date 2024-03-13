import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from src.apps.users.models import Role

COUNT_MINOR_EMPLOYEES_SUPERVISOR_FIRST = 22
COUNT_MINOR_EMPLOYEES_SUPERVISOR_SECOND = 14


@pytest.fixture
def supervisor_role():
    """Роль руководителя."""
    return Role.objects.create(name="supervisor")


@pytest.fixture
def employee_role():
    """Роль линейного сотрудника."""
    return Role.objects.create(name="employee")


@pytest.fixture
def supervisor_first(django_user_model, supervisor_role):
    """Первый руководитель."""
    return django_user_model.objects.create(
        username="supervisor_first", role=supervisor_role
    )


@pytest.fixture
def supervisor_first_token(supervisor_first):
    return Token.objects.create(user=supervisor_first)


@pytest.fixture
def supervisor_first_client(supervisor_first_token):
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f"Token {supervisor_first_token.key}"
    )
    return client


@pytest.fixture
def supervisor_second(django_user_model, supervisor_role):
    """Второй руководитель."""
    return django_user_model.objects.create(
        username="supervisor_second", role=supervisor_role
    )


@pytest.fixture
def supervisor_second_token(supervisor_second):
    return Token.objects.create(user=supervisor_second)


@pytest.fixture
def supervisor_second_client(supervisor_second_token):
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f"Token {supervisor_second_token.key}"
    )
    return client


@pytest.fixture
def employee_first(django_user_model, supervisor_first, employee_role):
    """Первый линейный сотрудник."""
    return django_user_model.objects.create(
        username="employee_first",
        first_name="employee_firstname_first",
        last_name="employee_lastname_first",
        role=employee_role,
        supervisor=supervisor_first,
    )


@pytest.fixture
def employee_first_token(employee_first):
    return Token.objects.create(user=employee_first)


@pytest.fixture
def employee_first_client(employee_first_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {employee_first_token.key}")
    return client


@pytest.fixture
def employee_second(django_user_model, supervisor_second, employee_role):
    """Второй линейный сотрудник."""
    return django_user_model.objects.create(
        username="employee_second",
        first_name="employee_firstname_second",
        last_name="employee_lastname_second",
        role=employee_role,
        supervisor=supervisor_second,
    )


@pytest.fixture
def employee_second_token(employee_second):
    return Token.objects.create(user=employee_second)


@pytest.fixture
def employee_second_client(employee_second_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {employee_second_token.key}")
    return client


@pytest.fixture
def minor_employees(
    django_user_model,
    supervisor_first,
    supervisor_second,
    employee_role,
):
    all_employees = []
    for i in range(COUNT_MINOR_EMPLOYEES_SUPERVISOR_FIRST):
        employee = django_user_model(
            username=f"s1_minor_employee_{i}",
            supervisor=supervisor_first,
            role=employee_role,
        )
        all_employees.append(employee)

    for i in range(COUNT_MINOR_EMPLOYEES_SUPERVISOR_SECOND):
        employee = django_user_model(
            username=f"s2_minor_employee_{i}",
            supervisor=supervisor_second,
            role=employee_role,
        )
        all_employees.append(employee)

    django_user_model.objects.bulk_create(all_employees)
