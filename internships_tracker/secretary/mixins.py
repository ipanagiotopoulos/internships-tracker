from django.shortcuts import redirect
from datetime import date
from .models import *
from carrier.models import CarrierAssignmentPeriod


class ApplicationPeriodFinished:

    def dispatch(self, request, *args, **kwargs):
        uni_department = self.request.GET.get('department', None)
        cas = CarrierAssignmentPeriod.objects.filter(
            department=uni_department
        ).first()
        if cas and cas.from_date <= date.today() <= cas.to_date:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/carrier/carrier-assignment/not-found")


class CarrierAssignmenetPeriodFinished:

    def dispatch(self, request, *args, **kwargs):
        uni_department = self.request.GET.get('department', None)
        cas = CarrierAssignmentPeriod.objects.filter(
            department=uni_department
        ).first()
        if cas and cas.from_date <= date.today() <= cas.to_date:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect("/carrier/carrier-assignment/not-found")
