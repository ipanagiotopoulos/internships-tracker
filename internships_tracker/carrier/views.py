from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DetailView, ListView, DeleteView, UpdateView, CreateView
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.db.models import Q
from django.http import Http404
from dal import autocomplete as auto
from datetime import date
from .forms import *
from .models import *
from .filters import TraineePositionsFilter
from internships_app.models import CarrierNode
from .mixins import CarrierAssignmentRequiredMixin, CarrierRequiredMixin, StudentOrCarrierRequiredMixin
from applicant.models import InternshipReport
# Create your views here.


def carrier_assignment_not_found(request):
    return render(request, 'carrier_assignment_not_found.html')


deps = ['IT', 'ND', 'ESD', 'G']


class TraineePositionListView(CarrierRequiredMixin, ListView):
    model = TraineePosition
    template_name = "trainee_positions.html"
    context_object_name = "tps"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department_request = self.request.GET.get(
            "carrier_assignment__department")
        user = self.request.user
        if department_request not in deps:
            raise Http404
        carrier_profile = CarrierNode.objects.filter(
            user_ptr_id=user.id).first()
        tp_queryset = TraineePosition.objects.filter(
            carrier_assignment__department=department_request, carrier=carrier_profile.carrier)
        myFilter = TraineePositionsFilter(
            self.request.GET, queryset=tp_queryset)
        context['filter'] = myFilter
        carrier_assignment_period = CarrierAssignmentPeriod.objects.filter(
            department=department_request).first()
        if (carrier_assignment_period != None) and (carrier_assignment_period.from_date <= date.today() <= carrier_assignment_period.to_date):
            context['assignment_period'] = True
        else:
            context['assignment_period'] = False
        return context

    def render_to_response(self, context):
        department_request = self.request.GET.get(
            "carrier_assignment__department")
        carrier_assignement_check = CarrierAssignmentPeriod.objects.filter(
            department=department_request).first() != None
        if carrier_assignement_check == False:
            return redirect('carrier:carrier_assignment_not_found')
        return super().render_to_response(context)


class TraineePositionCreateView(CarrierAssignmentRequiredMixin, CarrierRequiredMixin, CreateView):
    model = TraineePosition
    form_class = TraineePositionForm
    template_name = "trainee_position_create.html"
    success_url = "/carrier/traineepositions/list"

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        department = self.request.GET.get("department")
        if department not in deps:
            raise Http404
        return form

    def form_valid(self, form):
        carrier_node = CarrierNode.objects.get(
            user_ptr_id=self.request.user.id)
        uni_department = self.request.GET.get("department")
        ca = CarrierAssignmentPeriod.objects.get(
            department=uni_department
        )
        form.instance.carrier = carrier_node.carrier
        form.instance.carrier_assignment = ca
        return super().form_valid(form)

    def get_success_url(self):
        uni_department = self.request.GET.get("department")
        return '/carrier/traineepositions/list?carrier_assignment__department='+uni_department


class TraineePositionDetailView(StudentOrCarrierRequiredMixin, DetailView):
    model = TraineePosition
    template_name = "trainee_position.html"
    context_object_name = "trainee_position"


class TraineePositionDeleteView(UserPassesTestMixin, CarrierAssignmentRequiredMixin, CarrierRequiredMixin, DeleteView):
    model = TraineePosition
    template_name = "trainee_position_delete.html"
    context_object_name = "tp"

    def test_func(self):
        carrier_node = CarrierNode.objects.get(
            user_ptr_id=self.request.user.id)
        if self.get_object().finalized == True:
            raise PermissionDenied()
        if self.get_object().carrier == carrier_node.carrier:
            return True
        return False

    def get_success_url(self):
        department = self.request.GET.get('department')
        return "/carrier/traineepositions/list?carrier_assignment__department="+department


class TraineePositionUpdateView(UserPassesTestMixin, CarrierAssignmentRequiredMixin, CarrierRequiredMixin, UpdateView):
    model = TraineePosition
    form_class = TraineePositionForm
    template_name = "trainee_position_update.html"
    group_required = u"carrier_node"

    def test_func(self):
        carrier_node = CarrierNode.objects.get(
            user_ptr_id=self.request.user.id)
        if self.get_object().finalized == True:
            raise PermissionDenied()
        if self.get_object().carrier == carrier_node.carrier:
            return True
        return False

    def get_success_url(self):
        department_request = self.request.GET.get("department")
        if department_request not in deps:
            raise Http404
        return "/carrier/traineepositions/list?carrier_assignment__department="+department_request


class AsssignmentListView(ListView, CarrierRequiredMixin):
    model = Assignment
    template_name = "assignments.html"
    context_object_name = "assignments"

    def get_queryset(self):
        department = self.request.GET.get("department")
        if department not in deps:
            raise Http404
        carrier_node = CarrierNode.objects.filter(
            user_ptr_id=self.request.user.id).first()
        return Assignment.objects.filter(
            trainee_position__carrier__official_name=carrier_node.carrier.official_name, assignment_period__department=department, assignment_status="P",
            finalized=True)


class AsssignmentDetailView(UserPassesTestMixin, CarrierRequiredMixin, DetailView):
    model = Assignment
    template_name = "assignment_detail.html"
    context_object_name = "assignment"

    def test_func(self):
        department_request = self.request.GET.get("department")
        if department_request not in deps:
            raise Http404
        carrier_node = CarrierNode.objects.get(
            user_ptr_id=self.request.user.id)
        if self.get_object().trainee_position.carrier == carrier_node.carrier and self.get_object().finalized == True:
            return True
        return False


def assignment_accept(request, pk):
    department_request = request.GET.get("department")
    if department_request not in deps:
        raise Http404
    carrier_node = CarrierNode.objects.get(user_ptr_id=request.user.id)
    assignment = get_object_or_404(Assignment, pk=pk)
    if assignment.trainee_position.carrier == carrier_node.carrier and assignment.finalized == True:
        if CarrierConsent.objects.filter(Q(assignement_upon=assignment) & Q(consent=True)).exists():
            context = {
                'message': 'Carrier consent already exists !',
                'assignment': assignment
            }
            return render(request, 'assignment_detail.html', context)
        else:
            assignment.assignment_status = "A"
            assignment.save()
            CarrierConsent.objects.create(
                carrier=assignment.trainee_position.carrier, assignement_upon=assignment, consent=True)
            return redirect('/carrier/assignments?department='+department_request)
    else:
        raise PermissionDenied()


def assignment_reject(request, pk):
    carrier_node = CarrierNode.objects.get(user_ptr_id=request.user.id)
    assignment = get_object_or_404(Assignment, pk=pk)
    department_request = request.GET.get("department")
    if department_request not in deps:
        raise Http404
    if assignment.trainee_position.carrier == carrier_node.carrier and assignment.finalized == True:
        if CarrierConsent.objects.filter(assignement_upon=assignment).exists():
            context = {
                'message': 'Carrier consent already exists !',
                'assignment': assignment
            }
            return render(request, 'assignment_detail.html', context)
        else:
            assignment.assignment_status = "R"
            assignment.save()
            CarrierConsent.objects.create(
                carrier=assignment.trainee_position.carrier, assignement_upon=assignment, consent=False)
            return redirect('carrier:assignments?department='+department_request)
    else:
        raise PermissionDenied()


class AcceptedAsssignmentListView(CarrierRequiredMixin, ListView):
    model = Assignment
    template_name = "accepted_assignments.html"
    context_object_name = "assignments"

    def get_queryset(self):
        carrier_node = CarrierNode.objects.filter(
            id=self.request.user.id).first()

        return Assignment.objects.filter(Q(trainee_position__carrier=carrier_node.carrier) & Q(assignment_status='A') & Q(finalized=True))


class AcceptedAsssignmentDetailView(CarrierRequiredMixin, UserPassesTestMixin, DetailView):
    model = Assignment
    template_name = "accepted_assignment_detail.html"
    context_object_name = "assignment"

    def test_func(self):
        carrier_node = CarrierNode.objects.get(
            user_ptr_id=self.request.user.id)
        if self.get_object().trainee_position.carrier == carrier_node.carrier:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assignment = self.get_object()
        context["assignment"] = assignment
        report = InternshipReport.objects.filter(assignment=assignment)
        if report.exists():
            context["report"] = report.first()
        assesment = CarrierAssesement.objects.filter(
            assignement_upon=assignment)
        if assesment.exists():
            context["assesment"] = assesment.first()
        return context


class CarrierAssesementCreateView(CarrierRequiredMixin, CreateView):
    model = CarrierAssesement
    fields = ['comments', 'grade', 'assesment_file', 'report_essay_file']
    template_name = "carrier_assesment_create.html"

    def form_valid(self, form):
        form.instance.assignement_upon = Assignment.objects.get(
            id=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("carrier:accepted_assignment_detail", kwargs={'pk': self.kwargs.get('pk')})


class TraineePositionAutocomplete(StudentOrCarrierRequiredMixin, auto.Select2QuerySetView):
    def get_queryset(self):
        tr1 = self.forwarded.get("trainee_position_1", None)
        tr2 = self.forwarded.get("trainee_position_2", None)
        tr3 = self.forwarded.get("trainee_position_3", None)
        tr4 = self.forwarded.get("trainee_position_4", None)
        tr5 = self.forwarded.get("trainee_position_5", None)
        student = UndergraduateStudent.objects.get(
            user_ptr_id=self.request.user.id)

        qs = TraineePosition.objects.filter(
            carrier_assignment__department=student.department, finalized=True
        ).distinct('job_code').order_by('job_code')
        if tr1:
            traine1 = TraineePosition.objects.get(id=tr1)
            qs = qs.exclude(job_code=traine1.job_code)
        if tr2:
            traine2 = TraineePosition.objects.get(id=tr2)
            qs = qs.exclude(job_code=traine2.job_code)
        if tr3:
            traine3 = TraineePosition.objects.get(id=tr3)
            qs = qs.exclude(job_code=traine3.job_code)
        if tr4:
            traine4 = TraineePosition.objects.get(id=tr4)
            qs = qs.exclude(job_code=traine4.job_code)
        if tr5:
            traine5 = TraineePosition.objects.get(id=tr5)
            qs = qs.exclude(job_code=traine5.job_code)
        if self.q:
            qs = qs.filter(
                Q(title__icontains=self.q)
                | Q(carrier__official_name__icontains=self.q)
            )
        return qs


class CarrierDetailView(CarrierRequiredMixin, DetailView):
    model = Carrier
    template_name = "carrier_detail.html"
    context_object_name = "carrier"

    def get_object(self):
        carrier_node = CarrierNode.objects.get(
            user_ptr_id=self.request.user.id)
        return carrier_node.carrier


class CarrierUpdateView(CarrierRequiredMixin, UpdateView):
    model = Carrier
    form_class = CarrierUpdateForm
    template_name = "carrier_update.html"
    context_object_name = "carrier"

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields["country"].initial = self.object.full_address.country
        form.fields["city"].initial = self.object.full_address.city
        form.fields["street_name"].initial = self.object.full_address.street_name
        form.fields["street_number"].initial = self.object.full_address.street_number
        form.fields["postal_code"].initial = self.object.full_address.postal_code
        form.fields["department_1"].initial = self.object.department_1
        form.fields["department_2"].initial = self.object.department_2
        form.fields["department_3"].initial = self.object.department_3
        form.fields["department_4"].initial = self.object.department_4
        return form

    def form_valid(self, form):
        saved_form = form.save(commit=False)
        saved_form.full_address.country = form.cleaned_data["country"],
        saved_form.full_address.city = form.cleaned_data["city"],
        saved_form.full_address.street_name = form.cleaned_data["street_name"],
        saved_form.full_address.street_number = form.cleaned_data["street_number"],
        saved_form.full_address.postal_code = form.cleaned_data["postal_code"],
        saved_form.save()
        return super().form_valid(saved_form)

    def get_success_url(self):
        return reverse("carrier:carrier_detail")

    def get_object(self):
        carrier_node = CarrierNode.objects.get(
            user_ptr_id=self.request.user.id)
        return carrier_node.carrier
