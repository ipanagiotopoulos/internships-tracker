from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from internships_app.models import Carrier, UndergraduateStudent, Supervisor
from carrier.enums import APPLICATION_STATUS
from internships_app.enums import (
    DEPARTMENT_CHOICES, DEPARTMENT_CHOICES_CN
)
from utils.validators import alphabetic


class CarrierAssignmentPeriod(models.Model):
    department = models.CharField(
        unique=True, max_length=3, choices=DEPARTMENT_CHOICES_CN)
    from_date = models.DateField()
    to_date = models.DateField()

    def __str__(self):
        return self.department


class ApplicationPeriod(models.Model):
    department = models.CharField(
        unique=True, max_length=3, choices=DEPARTMENT_CHOICES_CN)
    from_date = models.DateField()
    to_date = models.DateField()

    def __str__(self):
        return self.department


class AssignmentPeriod(models.Model):
    department = models.CharField(
        unique=True, max_length=3, choices=DEPARTMENT_CHOICES_CN)
    from_date = models.DateField()
    to_date = models.DateField()
    complementary = models.BooleanField(default=False)

    def __str__(self):
        return self.department


class InternshipReportPeriod(models.Model):
    department = models.CharField(
        unique=True, max_length=3, choices=DEPARTMENT_CHOICES_CN)
    from_date = models.DateField()
    to_date = models.DateField()

    def __str__(self):
        return self.department


class TraineePosition(models.Model):
    title = models.CharField(max_length=200)
    job_code = models.CharField(max_length=100)
    no_id = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)])
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)
    carrier_assignment = models.ForeignKey(
        CarrierAssignmentPeriod, on_delete=models.CASCADE
    )
    supervisor = models.CharField(max_length=100, validators=[alphabetic])
    description = models.TextField(max_length=1500)
    created = models.DateTimeField(auto_now_add=True)
    finalized = models.BooleanField(default=False)

    class Meta:
        unique_together = ('job_code', 'no_id')

    def __str__(self):
        return self.job_code+":"+str(self.no_id)+" "+self.title + " in "+self.carrier.official_name


class Assignment(models.Model):
    date = models.DateField(auto_now_add=True)
    trainee = models.OneToOneField(
        UndergraduateStudent, unique=True,  on_delete=models.CASCADE)
    trainee_position = models.ForeignKey(
        TraineePosition, unique=True, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    assignment_period = models.ForeignKey(
        AssignmentPeriod, on_delete=models.CASCADE)
    finalized = models.BooleanField(default=False)
    assignment_status = models.CharField(
        max_length=1, choices=APPLICATION_STATUS, default="P")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.trainee.register_number+", "+self.trainee_position.title+", "+self.trainee_position.carrier.official_name


class CarrierConsent(models.Model):
    date = models.DateField(auto_now_add=True)
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)
    assignement_upon = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    consent = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.assignement_upon.trainee.register_number+","+self.assignement_upon.trainee_position.title


class CarrierAssesement(models.Model):
    assesment_file = models.FileField()
    report_essay_file = models.FileField()
    date = models.DateField(auto_now_add=True)
    assignement_upon = models.OneToOneField(
        Assignment, on_delete=models.CASCADE)
    comments = models.TextField(max_length=1000)
    finalized = models.BooleanField(default=False)
    grade = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.assignement_upon.trainee.register_number+", "+self.assignement_upon.trainee_position.title+", "+self.assignement_upon.trainee_position.carrier.official_name
