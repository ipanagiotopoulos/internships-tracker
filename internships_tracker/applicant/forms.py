from django import forms
from django.utils.safestring import mark_safe
from dal import autocomplete
from applicant.models import Preference
from carrier.models import TraineePosition


class PreferenceForm(forms.ModelForm):
    trainee_position_1 = forms.ModelChoiceField(
        required=False,
        queryset=TraineePosition.objects.all(),
        label=mark_safe("<strong> <h5> Trainee position 1 </h5> </strong>"),
        widget=autocomplete.ModelSelect2(
            url="carrier:traineeposition_autocomple",
            forward=[
                "trainee_position_2",
                "trainee_position_3",
                "trainee_position_4",
                "trainee_position_5",
            ],
            attrs={"data-width": "100%"},
        ),
    )
    trainee_position_2 = forms.ModelChoiceField(
        required=False,
        queryset=TraineePosition.objects.all(),
        label=mark_safe("<strong> <h5> Trainee position 2 </h5> </strong>"),
        widget=autocomplete.ModelSelect2(
            url="carrier:traineeposition_autocomple",
            forward=[
                "trainee_position_1",
                "trainee_position_3",
                "trainee_position_4",
                "trainee_position_5",
            ],
            attrs={"data-width": "100%"},
        ),
    )
    trainee_position_3 = forms.ModelChoiceField(
        required=False,
        queryset=TraineePosition.objects.all(),
        label=mark_safe("<strong> <h5> Trainee position 3 </h5> </strong>"),
        widget=autocomplete.ModelSelect2(
            url="carrier:traineeposition_autocomple",
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
        queryset=TraineePosition.objects.all(),
        label=mark_safe("<strong> <h5> Trainee position 4 </h5> </strong>"),
        widget=autocomplete.ModelSelect2(
            url="carrier:traineeposition_autocomple",
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
        queryset=TraineePosition.objects.all(),
        label=mark_safe("<strong> <h5> Trainee position 5 </h5> </strong>"),
        widget=autocomplete.ModelSelect2(
            url="carrier:traineeposition_autocomple",
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
        cleaned_data = super(PreferenceForm, self).clean()

        if not cleaned_data.get("trainee_position_1"):
            raise forms.ValidationError(
                {
                    "trainee_position_1": [
                        "You have to fill this field !",
                    ]
                }
            )
