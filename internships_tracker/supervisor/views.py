from .models import SupervisorAssesment
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from carrier.models import Assignment, CarrierAssesement
from internships_app.models import Supervisor
from applicant.models import InternshipReport
from .filters import SupervisorAssesmentFilter
from .forms import *


class AsssignmentListView(ListView):
    model = Assignment
    template_name = "supervisor_assignments.html"
    context_object_name = "assignments"

    def get_queryset(self):
        supervisor = Supervisor.objects.get(user_ptr_id=self.request.user.id)
        assesements = CarrierAssesement.objects.filter(
            assignement_upon__supervisor__id=supervisor.id, finalized=True)
        assignments = []
        for assesement in assesements:
            assignments.append(assesement.assignement_upon)
        return assignments


class AsssignmentDetailView(UserPassesTestMixin, DetailView):
    model = Assignment
    template_name = "supervisor_assignment_detail.html"
    context_object_name = "assignment"

    def test_func(self):
        supervisor = Supervisor.objects.get(user_ptr_id=self.request.user.id)
        if self.get_object().supervisor == supervisor:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assignment = self.get_object()
        context["assignment"] = assignment
        report = InternshipReport.objects.filter(assignment=assignment)
        if report.exists():
            context["report"] = report.first()
        carrier_assesment = CarrierAssesement.objects.filter(
            assignement_upon=assignment)
        print("Results are here: ca", carrier_assesment.first())
        if carrier_assesment.exists():
            context["carrier_assesment"] = carrier_assesment.first()
        supervisor_assesment = SupervisorAssesment.objects.filter(
            assignement_upon=assignment)
        print("Results are here: ca", supervisor_assesment.first())
        if supervisor_assesment.exists():
            context["supervisor_assesment"] = supervisor_assesment.first()
        return context


class SupervisorAssesmentCreateView(CreateView):
    model = SupervisorAssesment
    fields = ['comments', 'grade', 'assesment_file']
    template_name = "supervisor_assesment_create.html"

    def form_valid(self, form):
        form.instance.assignement_upon = Assignment.objects.get(
            id=self.kwargs.get('pk'))
        form.instance.supervisor = Supervisor.objects.get(
            user_ptr_id=self.request.user.id)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("supervisor:assignment_detail", kwargs={'pk': self.kwargs.get('pk')})


class SupervisorAssesmentListView(ListView):
    model = SupervisorAssesment
    context_object_name = "supervisor_assesements"
    template_name = "supervisor_assesements.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = Supervisor.objects.filter(
            user_ptr_id=self.request.user.id).first()
        sa_queryset = SupervisorAssesment.objects.filter(
            supervisor=user)
        myFilter = SupervisorAssesmentFilter(
            self.request.GET, queryset=sa_queryset)
        context = {'filter': myFilter}
        return context


class SupervisorAssesmentDetailView(DetailView):
    model = SupervisorAssesment
    context_object_name = "supervisor_assesement"
    template_name = "supervisor_assesement.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        supervisor_assesement = self.get_object()
        if supervisor_assesement.supervisor.user_ptr_id != self.request.user.id:
            raise PermissionDenied()
        return context


class SupervisorAssesmentUpdateView(UpdateView):
    model = SupervisorAssesment
    form_class = SupervisorAssesmentForm
    template_name = "supervisor_assesement_update.html"
    group_required = u"supervisor"

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        supervisor_assesement = self.get_object()
        if supervisor_assesement.supervisor.user_ptr_id != self.request.user.id:
            raise PermissionDenied()
        return form

    def get_success_url(self):
        return reverse("supervisor:assignments")
