from pytest_lazy_fixtures import lf

from tests.pytest_tests.fixtures.lms_fixtures import (
    COUNT_MINOR_LMS_FOR_EMPLOYEE_FIRST,
    COUNT_MINOR_LMS_FOR_EMPLOYEE_SECOND,
)
from tests.pytest_tests.fixtures.users_fixtures import (
    COUNT_MINOR_EMPLOYEES_SUPERVISOR_FIRST,
    COUNT_MINOR_EMPLOYEES_SUPERVISOR_SECOND,
)

users_test_00_parametrize = (
    "url_name, supervisor_client, employee_id",
    (
        ("api_v1:users-list", lf("supervisor_first_client"), None),
        ("api_v1:users-list", lf("supervisor_second_client"), None),
        ("api_v1:users-me", lf("supervisor_first_client"), None),
        ("api_v1:users-me", lf("supervisor_second_client"), None),
        (
            "api_v1:users-detail",
            lf("supervisor_first_client"),
            lf("employee_first.id"),
        ),
        (
            "api_v1:users-detail",
            lf("supervisor_second_client"),
            lf("employee_second.id"),
        ),
    ),
)

users_test_01_parametrize = (
    "supervisor_client, employees_count",
    (
        (
            lf("supervisor_first_client"),
            COUNT_MINOR_EMPLOYEES_SUPERVISOR_FIRST,
        ),
        (
            lf("supervisor_second_client"),
            COUNT_MINOR_EMPLOYEES_SUPERVISOR_SECOND,
        ),
    ),
)

users_test_02_parametrize = (
    "url_name, employee_client, employee",
    (
        (
            "api_v1:users-me",
            lf("employee_first_client"),
            lf("employee_first"),
        ),
        (
            "api_v1:users-me",
            lf("employee_second_client"),
            lf("employee_second"),
        ),
    ),
)

users_test_03_parametrize = (
    "url_name, employee_client, user_id",
    (
        (
            "api_v1:users-list",
            lf("employee_first_client"),
            None,
        ),
        (
            "api_v1:users-list",
            lf("employee_second_client"),
            None,
        ),
        (
            "api_v1:users-detail",
            lf("employee_first_client"),
            lf("employee_second.id"),
        ),
        (
            "api_v1:users-detail",
            lf("employee_first_client"),
            lf("supervisor_first.id"),
        ),
        (
            "api_v1:users-detail",
            lf("employee_second_client"),
            lf("employee_first.id"),
        ),
        (
            "api_v1:users-detail",
            lf("employee_second_client"),
            lf("supervisor_second.id"),
        ),
    ),
)

users_test_05_parametrize = (
    "supervisor_client, employee",
    (
        (lf("supervisor_first_client"), lf("employee_second")),
        (lf("supervisor_second_client"), lf("employee_first")),
    ),
)

lms_test_01_parametrize = (
    "supervisor_client, employee_id, lms_count",
    (
        (
            lf("supervisor_first_client"),
            lf("employee_first.id"),
            COUNT_MINOR_LMS_FOR_EMPLOYEE_FIRST,
        ),
        (
            lf("supervisor_second_client"),
            lf("employee_second.id"),
            COUNT_MINOR_LMS_FOR_EMPLOYEE_SECOND,
        ),
    ),
)

lms_test_06_parametrize = (
    "supervisor_client, employee_id",
    (
        (
            lf("supervisor_first_client"),
            lf("employee_second.id"),
        ),
        (
            lf("supervisor_second_client"),
            lf("employee_first.id"),
        ),
    ),
)
