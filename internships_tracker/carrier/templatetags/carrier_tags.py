from carrier.models import TraineePosition, ApplicationPeriod, CarrierAssignmentPeriod
from internships_app.models import CarrierNode
from django import template
import logging
from datetime import date

logger = logging.getLogger(__name__)

register = template.Library()


@register.simple_tag
def is_active(user):
    cn = CarrierNode.objects.get(id=user.id)
    cas = CarrierAssignmentPeriod.objects.filter(
        department=cn.carrier.department_1
    ).first()
    if cas == None:
        return False
    elif cas.from_date <= date.today() <= cas.to_date:
        return True
    return False


@register.simple_tag
def has_job_postings(user):
    cn = CarrierNode.objects.get(user_ptr_id=user.id)
    trainee_positions = TraineePosition.objects.filter(
        carrier=cn.carrier).first()
    if trainee_positions.exists():
        return True
    else:
        return False


@register.simple_tag
def is_application_approval_active(user):
    cn = CarrierNode.objects.get(user_ptr_id=user.id)
    cas = ApplicationPeriod.objects.filter(
        department=cn.carrier.department).first()
    if cas == None:
        return False
    elif cas.to_date < date.today():
        return True
    return False


@register.simple_tag
def all_carrier_uni_departments(user):
    dep_to_return = []
    cn = CarrierNode.objects.filter(user_ptr_id=user.id).first()
    if cn:
        if cn.carrier.department_1 != "NON":
            dep_to_return.append(cn.carrier.department_1)
        if cn.carrier.department_2 != "NON":
            dep_to_return.append(cn.carrier.department_2)
        if cn.carrier.department_3 != "NON":
            dep_to_return.append(cn.carrier.department_3)
        if cn.carrier.department_4 != "NON":
            dep_to_return.append(cn.carrier.department_4)
    else:
        dep_to_return = None
    return dep_to_return
