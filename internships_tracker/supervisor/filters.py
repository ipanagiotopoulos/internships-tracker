import django_filters
from .models import SupervisorAssesment


class SupervisorAssesmentFilter(django_filters.FilterSet):
    class Meta:
        model = SupervisorAssesment
        fields = {
            "finalized": ["exact"],
            "assignement_upon__trainee__register_number": ['exact'],
            "assignement_upon__trainee_position__title": ['icontains'],
        }
