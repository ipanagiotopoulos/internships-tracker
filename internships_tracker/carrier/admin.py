from django.contrib import admin
from .models import *
from django import forms

# Register your models here.
admin.site.register(TraineePosition)
admin.site.register(Assignment)
admin.site.register(CarrierConsent)
admin.site.register(CarrierAssesement)


class CarrierAssignmentPeriodForm(forms.ModelForm):
    class Meta:
        model = CarrierAssignmentPeriod
        fields = '__all__'

    def clean(self):
        from_date = self.cleaned_data.get('from_date')
        to_date = self.cleaned_data.get('to_date')
        if from_date > to_date:
            raise forms.ValidationError("Dates are incorrect")
        return self.cleaned_data


class CarrierAssignmentPeriodAdmin(admin.ModelAdmin):
    form = CarrierAssignmentPeriodForm


admin.site.register(CarrierAssignmentPeriod, CarrierAssignmentPeriodAdmin)


class ApplicationPeriodForm(forms.ModelForm):
    class Meta:
        model = ApplicationPeriod
        fields = '__all__'

    def clean(self):
        from_date = self.cleaned_data.get('from_date')
        to_date = self.cleaned_data.get('to_date')
        if from_date > to_date:
            raise forms.ValidationError("Dates are incorrect")

        uni_department = self.cleaned_data.get('department')
        cas = CarrierAssignmentPeriod.objects.filter(
            department=uni_department
        ).first()
        if cas:
            if cas.to_date > from_date:
                raise forms.ValidationError("Periods conflict on Department "+uni_department+" starting date of Application Period: "+str(
                    from_date)+" and ending date for Carrier Assignment: "+str(cas.to_date))
        else:
            raise forms.ValidationError(
                "Carrier Assignment Period does not exist")
        return self.cleaned_data


class ApplicationPeriodAdmin(admin.ModelAdmin):
    form = ApplicationPeriodForm


admin.site.register(ApplicationPeriod, ApplicationPeriodAdmin)


class AssignmentPeriodForm(forms.ModelForm):
    class Meta:
        model = AssignmentPeriod
        fields = '__all__'

    def clean(self):
        from_date = self.cleaned_data.get('from_date')
        to_date = self.cleaned_data.get('to_date')
        if from_date > to_date:
            raise forms.ValidationError("Dates are incorrect")
        uni_department = self.cleaned_data.get('department')
        app_period = ApplicationPeriod.objects.filter(
            department=uni_department
        ).first()
        if app_period:
            if app_period.to_date > from_date:
                raise forms.ValidationError("Periods conflict on Department "+uni_department+" starting date of Assignment Period: "+str(
                    from_date)+" and ending date for applications: "+str(app_period.to_date))
        else:
            raise forms.ValidationError("Application Period does not exist")
        return self.cleaned_data


class AssignmentPeriodAdmin(admin.ModelAdmin):
    form = AssignmentPeriodForm


admin.site.register(AssignmentPeriod, AssignmentPeriodAdmin)


class InternshipReportPeriodForm(forms.ModelForm):
    class Meta:
        model = InternshipReportPeriod
        fields = '__all__'

    def clean(self):
        from_date = self.cleaned_data.get('from_date')
        to_date = self.cleaned_data.get('to_date')
        if from_date > to_date:
            raise forms.ValidationError("Dates are incorrect")
        uni_department = self.cleaned_data.get('department')
        assignment_period = AssignmentPeriod.objects.filter(
            department=uni_department
        ).first()
        if assignment_period:
            if assignment_period.to_date > from_date:
                raise forms.ValidationError("Periods conflict on Department "+uni_department+" starting date of Internship Reports Period: "+str(
                    from_date)+" and ending date for assignments: "+str(assignment_period.to_date))
        else:
            raise forms.ValidationError("Assignment Period does not  exist")
        return self.cleaned_data


class InternshipReportPeriodAdmin(admin.ModelAdmin):
    form = InternshipReportPeriodForm


admin.site.register(InternshipReportPeriod, InternshipReportPeriodAdmin)
