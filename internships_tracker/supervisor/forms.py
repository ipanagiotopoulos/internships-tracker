from .models import SupervisorAssesment
import datetime
from django import forms


class SupervisorAssesmentForm(forms.ModelForm):
    comments = forms.CharField(max_length=5000, required=True)
    grade = forms.IntegerField(min_value=0, max_value=10)

    class Meta:
        model = SupervisorAssesment
        fields = ("comments", "assesment_file", "grade")
