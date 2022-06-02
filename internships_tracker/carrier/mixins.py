from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from datetime import date
from .models import *


class CarrierAssignmentRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        uni_department = self.request.GET.get('department', None)
        cas = CarrierAssignmentPeriod.objects.filter(
            department=uni_department
        ).first()
        if cas and cas.from_date <= date.today() <= cas.to_date:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/carrier/carrier-assignment/not-found")


class CarrierRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        for g in user.groups.all():
            if g.name == "carrier_node":
                return super().dispatch(request, *args, **kwargs)

        return HttpResponseNotFound("Not found")


class StudentOrCarrierRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        for g in user.groups.all():
            if g.name == "student" or g.name == "carrier_node" or g == "secretarian":
                return super().dispatch(request, *args, **kwargs)

        return HttpResponseNotFound("Not found")
