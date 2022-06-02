from internships_app.models import Secratarian
from django.core.exceptions import PermissionDenied


def return_url(request, basic_list_view_url):
    if request.META.get('HTTP_REFERER') == None:
        return basic_list_view_url
    return str(request.META.get('HTTP_REFERER'))


def secretarian_department_select(user_id):
    secretarian = Secratarian.objects.filter(
        user_ptr_id=user_id).first()
    if secretarian.department != "NONE" and secretarian.department != "ALL":
        return secretarian.department
    elif secretarian.department == "ALL":
        return "ALL"
    else:
        raise PermissionDenied()


def secretarian_department_item_select_object(user_id, object):
    secretarian = Secratarian.objects.filter(
        user_ptr_id=user_id).first()
    if secretarian.department == object.department:
        return True
    elif secretarian.department == "ALL":
        return True
    else:
        raise PermissionDenied()


def secretarian_department_item_select(user_id, department):
    secretarian = Secratarian.objects.filter(
        user_ptr_id=user_id).first()
    if secretarian.department == department:
        return True
    elif secretarian.department == "ALL":
        return True
    else:
        raise PermissionDenied()


def secretarian_carrier_department_item_select_object(user_id, carrier):
    secretarian = Secratarian.objects.filter(
        user_ptr_id=user_id).first()
    if secretarian.department in (carrier.department_1, carrier.department_2, carrier.department_3, carrier.department_4):
        return True
    elif secretarian.department == "ALL":
        return True
    else:
        raise PermissionDenied()
