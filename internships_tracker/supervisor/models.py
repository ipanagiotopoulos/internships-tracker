from internships_app.models import Supervisor
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from carrier.models import Assignment
# Create your models here.


class SupervisorAssesment(models.Model):
    date = models.DateField(auto_now_add=True)
    assesment_file = models.FileField()
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    assignement_upon = models.OneToOneField(
        Assignment, on_delete=models.CASCADE)
    comments = models.TextField(max_length=1500)
    finalized = models.BooleanField(default=False)
    grade = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    def __str__(self):
        return self.assignement_upon.supervisor.department+","+self.assignement_upon.supervisor.register_number+","+self.assignement_upon.trainee_position.title+","+self.assignement_upon.trainee_position.carrier.official_name
