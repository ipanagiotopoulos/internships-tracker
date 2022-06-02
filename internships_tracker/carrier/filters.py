import django_filters
from .models import TraineePosition, Assignment, CarrierConsent


class TraineePositionsFilter(django_filters.FilterSet):

    class Meta:
        model = TraineePosition
        fields = {
            'title': ['icontains'],
            'job_code': ['exact'],
            'no_id': ['exact'],
            'carrier_assignment__department': ['exact'],
        }


class AssignmentFilter(django_filters.FilterSet):

    class Meta:
        model = Assignment
        fields = {
            'trainee__first_name': ['icontains'],
            'trainee__last_name': ['icontains'],
            'trainee__department': ['exact'],
            'trainee_position__carrier__official_name': ['icontains'],
            'trainee_position__title':  ['exact'],
            'assignment_status': ['exact'],
        }
