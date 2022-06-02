from ..models import Preference, InternshipReport
from carrier.models import ApplicationPeriod, InternshipReportPeriod
from internships_app.models import UndergraduateStudent
from django import template
import logging
from datetime import date

logger = logging.getLogger(__name__)

register = template.Library()


@register.simple_tag
def has_preference(user):
    student = UndergraduateStudent.objects.get(user_ptr_id=user.id)
    if Preference.objects.filter(applicant=student).exists():
        return True
    return False


@register.simple_tag
def has_internship_period_student(user):
    student = UndergraduateStudent.objects.get(user_ptr_id=user.id)
    if InternshipReport.objects.filter(assignment__trainee=student).exists():
        return True
    return False


@register.simple_tag
def applicant_position_period(user):
    student = UndergraduateStudent.objects.get(user_ptr_id=user.id)
    application_period = ApplicationPeriod.objects.filter(
        department=student.department
    ).first()
    if application_period == None:
        return False
    elif application_period.from_date <= date.today() <= application_period.to_date:
        return True
    return False


@register.simple_tag
def applicant_internship_report_period(user):
    student = UndergraduateStudent.objects.get(user_ptr_id=user.id)
    internship_report_period = InternshipReportPeriod.objects.filter(
        department=student.department
    ).first()
    if internship_report_period == None:
        return False
    elif internship_report_period.from_date <= date.today() <= internship_report_period.to_date:
        return True
    return False
