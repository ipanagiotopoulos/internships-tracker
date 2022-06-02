import django_filters
from django import forms
from internships_app.models import CarrierNode, UndergraduateStudent
from carrier.models import TraineePosition, Assignment, CarrierAssesement
from applicant.models import Preference, InternshipReport
from supervisor.models import SupervisorAssesment


class CarrierNodeFilter(django_filters.FilterSet):

    class Meta:
        model = CarrierNode
        fields = {
            'first_name': ['icontains'],
            'last_name': ['icontains'],
            'is_active': ['exact'],
            'carrier__official_name': ['icontains'],
        }


class UndergraduateStudentFilter(django_filters.FilterSet):

    class Meta:
        model = UndergraduateStudent
        fields = {
            'first_name': ['icontains'],
            'last_name':  ['icontains'],
            'register_number': ['exact'],
            'department': ['exact'],
            'is_active': ['exact'],
        }


class TraineePositionsFilter(django_filters.FilterSet):

    class Meta:
        model = TraineePosition
        fields = {
            'title': ['icontains'],
            'finalized':  ['exact'],
            'job_code': ['icontains'],
            'carrier__official_name': ['exact'],
            'carrier_assignment__department': ['exact'],
            'no_id': ['exact'],
        }


class PreferencesFilter(django_filters.FilterSet):

    class Meta:
        model = Preference
        fields = {
            'applicant__first_name': ['icontains'],
            'applicant__last_name':  ['icontains'],
            'applicant__register_number': ['exact'],
            'finalized': ['exact'],
        }


class AssignmentFilter(django_filters.FilterSet):

    class Meta:
        model = Assignment
        fields = {
            'trainee__first_name': ['icontains'],
            'trainee__last_name': ['icontains'],
            'trainee__department': ['exact'],
            'finalized': ['exact'],
            'trainee_position__carrier__official_name': ['icontains'],
            'trainee_position__title':  ['exact'],
            'assignment_status': ['exact'],
        }


class InternshipsReportFilter(django_filters.FilterSet):
    class Meta:
        model = InternshipReport
        fields = {
            "finalized": ["exact"],
            "assignment__trainee__register_number": ['exact'],
            "assignment__trainee_position__title": ['icontains'],
        }


class CarrierAssesmentFilter(django_filters.FilterSet):
    class Meta:
        model = CarrierAssesement
        fields = {
            "finalized": ["exact"],
            "assignement_upon__trainee__register_number": ['exact'],
            "assignement_upon__trainee_position__title": ['icontains'],
        }


class SupervisorAssesmentFilter(django_filters.FilterSet):
    class Meta:
        model = SupervisorAssesment
        fields = {
            "finalized": ["exact"],
            "assignement_upon__trainee__register_number": ['exact'],
            "assignement_upon__trainee_position__title": ['icontains'],
        }
