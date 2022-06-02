from django.db import models
from carrier.models import TraineePosition, Assignment
from internships_app.models import UndergraduateStudent


class Preference(models.Model):
    applicant = models.OneToOneField(
        UndergraduateStudent, on_delete=models.CASCADE)
    trainee_position_1 = models.ForeignKey(
        TraineePosition,
        related_name="first_choice",
        verbose_name="First Choice",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    trainee_position_2 = models.ForeignKey(
        TraineePosition,
        related_name="second_choice",
        verbose_name="Second Choice",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    trainee_position_3 = models.ForeignKey(
        TraineePosition,
        related_name="third_choice",
        verbose_name="Third Choice",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    trainee_position_4 = models.ForeignKey(
        TraineePosition,
        related_name="fourth_choice",
        verbose_name="Fourth Choice",
        null=True,
        on_delete=models.CASCADE,
    )
    trainee_position_5 = models.ForeignKey(
        TraineePosition,
        related_name="fifth_choice",
        verbose_name="Fifth Choice",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    finalized = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.applicant.department+" "+self.applicant.register_number+" "+self.applicant.first_name+" "+self.applicant.last_name


class InternshipReport(models.Model):
    report_file = models.FileField()
    attendance_report_file = models.FileField()
    questionaire_file = models.FileField()
    assignment = models.OneToOneField(Assignment, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    finalized = models.BooleanField(default=False)
    comments = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.assignment.trainee.register_number+","+self.assignment.trainee_position.title+","+self.assignment.trainee_position.carrier.official_name
