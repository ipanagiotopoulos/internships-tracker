from django import forms
from .models import *
from internships_app.models import Carrier
from utils.validators import alphabetic


class TraineePositionForm(forms.ModelForm):
    title = forms.CharField(required=True, max_length=200, min_length=5)
    description = forms.CharField(
        required=True, max_length=1500, min_length=10, widget=forms.Textarea
    )
    no_id = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(99999)])
    job_code = forms.CharField(required=True, max_length=100, min_length=2)

    class Meta:
        model = TraineePosition
        fields = (
            "title",
            "description",
            "supervisor",
            "no_id",
            "job_code",
        )


class CreateCarrierAssementForm(forms.ModelForm):
    class Meta:
        model = CarrierAssesement
        fields = (
            "assignement_upon",
            "comments",
            "grade",
            "assesment_file",
        )


class CarrierUpdateForm(forms.ModelForm):
    country = forms.CharField(max_length=30, validators=[
                              alphabetic], required=True)
    city = forms.CharField(max_length=40, validators=[
                           alphabetic], required=True)
    street_name = forms.CharField(max_length=100, validators=[
                                  alphabetic], required=True)
    street_number = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(9999)], required=True
    )
    postal_code = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(99999)], required=True
    )
    department_1 = forms.ChoiceField(choices=DEPARTMENT_CHOICES, disabled=True)
    department_2 = forms.ChoiceField(choices=DEPARTMENT_CHOICES, disabled=True)
    department_3 = forms.ChoiceField(choices=DEPARTMENT_CHOICES, disabled=True)
    department_4 = forms.ChoiceField(choices=DEPARTMENT_CHOICES, disabled=True)

    class Meta:
        model = Carrier
        fields = (
            "official_name",
            "description",
        )
