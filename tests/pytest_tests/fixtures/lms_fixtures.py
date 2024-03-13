import datetime

import pytest

from src.apps.lms.models import LMS

COUNT_MINOR_LMS_FOR_EMPLOYEE_FIRST = 6
COUNT_MINOR_LMS_FOR_EMPLOYEE_SECOND = 11


@pytest.fixture
def lms_first(employee_first, supervisor_first):
    return LMS.objects.create(
        name="lms_first",
        description="lms_first_description",
        is_active=True,
        deadline=datetime.datetime.now().date() + datetime.timedelta(days=30),
        status="in_progress",
        skill_assessment_before=3,
        skill_assessment_after=5,
        employee=employee_first,
        supervisor=supervisor_first,
    )


@pytest.fixture
def minor_lms(
    employee_first,
    supervisor_first,
    employee_second,
    supervisor_second,
):
    _minor_lms = []
    for i in range(COUNT_MINOR_LMS_FOR_EMPLOYEE_FIRST):
        lms = LMS(
            name=f"lms_first_employee_1_{i}",
            description="lms_first_description_employee_1",
            is_active=False,
            deadline=datetime.datetime.now().date()
            + datetime.timedelta(days=1 + i),
            status="in_progress",
            skill_assessment_before=3,
            skill_assessment_after=5,
            employee=employee_first,
            supervisor=supervisor_first,
        )
        _minor_lms.append(lms)

    for i in range(COUNT_MINOR_LMS_FOR_EMPLOYEE_SECOND):
        lms = LMS(
            name=f"lms_first_employee_2{i}",
            description="lms_first_description_employee_2",
            is_active=False,
            deadline=datetime.datetime.now().date()
            + datetime.timedelta(days=1 + i),
            status="in_progress",
            skill_assessment_before=3,
            skill_assessment_after=5,
            employee=employee_second,
            supervisor=supervisor_second,
        )
        _minor_lms.append(lms)

    return LMS.objects.bulk_create(_minor_lms)
