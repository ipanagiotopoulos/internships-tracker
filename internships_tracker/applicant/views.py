from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from datetime import date
from .mixins import ApplicationPeriodRequiredMixin, InternshipReportPeriodRequiredMixin
from carrier.models import CarrierConsent, Assignment
from internships_app.models import UndergraduateStudent
from carrier.models import TraineePosition, Assignment, InternshipReportPeriod, ApplicationPeriod
from .forms import PreferenceForm
from .models import Preference, InternshipReport


def application_period_not_found(request):
    return render(request, 'application_period_not_found.html')


def report_period_not_found(request):
    return render(request, 'report_period_not_found.html')


class CreatePreferenceView(ApplicationPeriodRequiredMixin, CreateView):
    model = Preference
    form_class = PreferenceForm
    template_name = "preference_create.html"
    success_url = "/studentapplications/application/my"

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        student = UndergraduateStudent.objects.get(
            user_ptr_id=self.request.user.id)
        for i in range(1, 5):
            form.fields[
                "trainee_position_" + str(i)
            ].queryset = TraineePosition.objects.filter(
                carrier_assignment__department=student.department,
                finalized=True
            ).distinct('job_code').order_by()

        return form

    def form_valid(self, form):
        student = UndergraduateStudent.objects.get(
            user_ptr_id=self.request.user.id)
        form.instance.applicant = student
        return super().form_valid(form)


class PreferenceUpdateView(ApplicationPeriodRequiredMixin, UpdateView):
    model = Preference
    context_object_name = "preference"
    template_name = "preference_update.html"
    form_class = PreferenceForm
    success_url = "/studentapplications/application/my"

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        student = UndergraduateStudent.objects.get(
            user_ptr_id=self.request.user.id)
        for i in range(1, 5):
            form.fields[
                "trainee_position_" + str(i)
            ].queryset = TraineePosition.objects.filter(
                carrier_assignment__department=student.department, finalized=True
            ).distinct('job_code').order_by()
        return form

    def get_object(self):
        student = UndergraduateStudent.objects.get(
            user_ptr_id=self.request.user.id)
        return Preference.objects.get(applicant=student)


class PreferenceDetailView(DetailView):
    model = Preference
    context_object_name = "preference"
    template_name = "preference_detail.html"

    def get_object(self):
        student = UndergraduateStudent.objects.get(
            user_ptr_id=self.request.user.id)
        preference = Preference.objects.filter(applicant=student)
        if preference.exists():
            return preference.first()
        return None


class TraineePositionStudentListView(ApplicationPeriodRequiredMixin, ListView):
    model = TraineePosition
    context_object_name = "tps"
    paginate_by = 5
    paginate_orphans = 3
    template_name = "student_trainee_positions.html"

    def get_queryset(self):
        student = UndergraduateStudent.objects.get(
            user_ptr_id=self.request.user.id)
        student_dep_application_period = ApplicationPeriod.objects.filter(
            department=student.department).first()
        if student_dep_application_period and student_dep_application_period.from_date <= date.today() <= student_dep_application_period.to_date:
            return TraineePosition.objects.filter(carrier_assignment__department=student.department, finalized=True).distinct('job_code')


class MyCarrierConsentDetailView(DetailView):
    model = CarrierConsent
    context_object_name = "carrier_consent"
    template_name = "my_carrier_consent.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = UndergraduateStudent.objects.get(
            user_ptr_id=self.request.user.id)
        report = InternshipReport.objects.filter(assignment__trainee=student)
        if report.exists():
            context["report"] = report.first()
        context["carrier_consent"] = self.get_object()
        return context

    def get_object(self):
        student = UndergraduateStudent.objects.get(
            user_ptr_id=self.request.user.id)
        carrier_consent = CarrierConsent.objects.filter(
            assignement_upon__trainee=student, assignement_upon__finalized=True, consent=True)
        if carrier_consent.exists():
            return carrier_consent.first()
        return None


class InternshipReportCreateView(InternshipReportPeriodRequiredMixin, CreateView):
    model = InternshipReport
    fields = ['attendance_report_file',
              'questionaire_file', 'report_file', 'comments', ]
    template_name = "report_create.html"

    def form_valid(self, form):
        form.instance.assignment = Assignment.objects.get(
            pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = UndergraduateStudent.objects.get(
            user_ptr_id=self.request.user.id)
        context["assignment"] = Assignment.objects.get(
            pk=self.kwargs.get('pk'))
        context["report_period"] = InternshipReportPeriod.objects.filter(
            department=student.department)
        return context

    def get_success_url(self):
        return reverse('applicant:my_carrier_consent')


class InternshipReportUpdateView(UserPassesTestMixin, InternshipReportPeriodRequiredMixin, UpdateView):
    model = InternshipReport
    fields = ['report_file', 'attendance_report_file',
              'questionaire_file', 'comments']
    template_name = "report_update.html"

    def test_func(self):
        student = UndergraduateStudent.objects.get(
            user_ptr_id=self.request.user.id)
        if self.get_object().assignment.trainee == student:
            return True
        return False

    def form_valid(self, form):
        form.instance.assignment = Assignment.objects.get(
            pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = UndergraduateStudent.objects.get(
            user_ptr_id=self.request.user.id)
        context["assignment"] = Assignment.objects.get(
            pk=self.kwargs.get('pk'))
        context["report_period"] = InternshipReportPeriod.objects.filter(
            department=student.department)
        return context

    def get_object(self):
        return InternshipReport.objects.get(pk=self.kwargs.get('report_id'))

    def get_success_url(self):
        return reverse('applicant:my_carrier_consent')
