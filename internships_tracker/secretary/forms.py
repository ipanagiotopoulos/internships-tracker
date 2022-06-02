from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from dal import autocomplete
from applicant.models import Preference
from carrier.models import TraineePosition, Assignment


class SecrataryPreferenceForm(forms.ModelForm):
    trainee_position_1 = forms.ModelChoiceField(
        required=False,
        queryset=TraineePosition.objects.none(),
        widget=autocomplete.ModelSelect2(
            url="secretary:sec_traineeposition_autocomple",
            forward=[
                "trainee_position_2",
                "trainee_position_3",
                "trainee_position_4",
                "trainee_position_5",
            ],
        ),
    )
    trainee_position_2 = forms.ModelChoiceField(
        required=False,
        queryset=TraineePosition.objects.none(),
        widget=autocomplete.ModelSelect2(
            url="secretary:sec_traineeposition_autocomple",
            forward=[
                "trainee_position_1",
                "trainee_position_3",
                "trainee_position_4",
                "trainee_position_5",
            ],
        ),
    )
    trainee_position_3 = forms.ModelChoiceField(
        required=False,
        queryset=TraineePosition.objects.none(),
        widget=autocomplete.ModelSelect2(
            url="secretary:sec_traineeposition_autocomple",
            forward=[
                "trainee_position_2",
                "trainee_position_1",
                "trainee_position_4",
                "trainee_position_5",
            ],
            attrs={"data-width": "100%"},
        ),
    )
    trainee_position_4 = forms.ModelChoiceField(
        required=False,
        queryset=TraineePosition.objects.none(),
        widget=autocomplete.ModelSelect2(
            url="secretary:sec_traineeposition_autocomple",
            forward=[
                "trainee_position_2",
                "trainee_position_3",
                "trainee_position_1",
                "trainee_position_5",
            ],
        ),
    )
    trainee_position_5 = forms.ModelChoiceField(
        required=False,
        queryset=TraineePosition.objects.none(),
        widget=autocomplete.ModelSelect2(
            url="secretary:sec_traineeposition_autocomple",
            forward=[
                "trainee_position_2",
                "trainee_position_3",
                "trainee_position_4",
                "trainee_position_1",
            ],
        ),
    )

    class Meta:
        model = Preference
        fields = (
            "trainee_position_1",
            "trainee_position_2",
            "trainee_position_3",
            "trainee_position_4",
            "trainee_position_5",
        )

    def clean(self):
        cleaned_data = super(SecrataryPreferenceForm, self).clean()

        if not cleaned_data.get("trainee_position_1"):
            raise forms.ValidationError(
                {
                    "trainee_position_1": [
                        "You have to fill this field !",
                    ]
                }
            )


class AssignmentSecretaryForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = (
            "trainee",
            "trainee_position",
            "supervisor",
            "assignment_period",
            "assignment_status",
        )


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
