from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DeleteView, UpdateView, CreateView, DetailView
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from datetime import date
from dal import autocomplete as auto
from internships_app.models import UndergraduateStudent, User, CarrierNode, Supervisor, Secratarian
from applicant.models import Preference, InternshipReport
from supervisor.models import SupervisorAssesment
from carrier.models import TraineePosition, CarrierAssignmentPeriod, Assignment, AssignmentPeriod, CarrierConsent, CarrierAssesement
from .forms import *
from .filters import CarrierNodeFilter, UndergraduateStudentFilter, TraineePositionsFilter, PreferencesFilter, AssignmentFilter, InternshipsReportFilter, CarrierAssesmentFilter, SupervisorAssesmentFilter
from .utils import return_url, secretarian_department_select, secretarian_department_item_select_object, secretarian_department_item_select, secretarian_carrier_department_item_select_object


deps = ['IT', 'ND', 'ESD', 'G']

carrier_node_approve_basic_list_view_url = "/secretary/carriers/registrations"
trainee_position_approve_basic_url = "/secretary/carriers/trainee_positions"
preferences_approve_basic_url = "/secretary/students/preferences"
assignment_approve_basic_url = "/secretary/assignments"


class ApprovalRejectionUndergraduateStudentListView(ListView):
    model = UndergraduateStudent
    context_object_name = "students"
    template_name = "students_registrations.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {
            'student_reg_message_result': self.request.session.pop('student_reg_message', None)
        }
        dep = secretarian_department_select(self.request.user.id)
        undergraduate_stud_queryset = UndergraduateStudent.objects.all().order_by("is_active") if dep == "ALL" else UndergraduateStudent.objects.filter(
            department=dep).order_by("is_active")
        myFilter = UndergraduateStudentFilter(
            self.request.GET, queryset=undergraduate_stud_queryset)
        context['filter'] = myFilter
        return context


def student_approval_rejection(request, pk):
    undergraduate_student = UndergraduateStudent.objects.filter(id=pk).first()
    if secretarian_department_item_select_object(request.user.id, undergraduate_student):
        req_user = User.objects.filter(
            id=undergraduate_student.user_ptr_id).first()
        context = {'req_user': req_user,
                   'student': undergraduate_student}
    return render(request, "undergraduate_student_app_rjc.html", context)


def student_approve(request, pk):
    undergraduate_student = UndergraduateStudent.objects.filter(id=pk).first()
    if secretarian_department_item_select_object(request.user.id, undergraduate_student):
        user = User.objects.filter(
            id=undergraduate_student.user_ptr_id).first()
        user.is_active = True
        user.save()
        request.session['student_reg_message'] = "User: " + \
            str(user)+" has been activated!"
    return redirect('secretary:sec_students_registrations')


def student_reject(request, pk):
    undergraduate_student = UndergraduateStudent.objects.filter(id=pk).first()
    if secretarian_department_item_select_object(request.user.id, undergraduate_student):
        user = User.objects.filter(
            id=undergraduate_student.user_ptr_id).first()
        undergraduate_student.delete()
        user.delete()
        request.session['student_reg_message'] = "User: " + \
            str(user)+" has been deleted!"
    return redirect('secretary:sec_students_registrations')


class ApprovalRejectionCarrierNodeListView(ListView):
    model = CarrierNode
    context_object_name = "carriers"
    template_name = "carrier_registrations.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dep = secretarian_department_select(self.request.user.id)
        print("department is here", dep)
        carrier_node_queryset = CarrierNode.objects.all() if dep == "ALL" else CarrierNode.objects.filter(
            Q(carrier__department_1=dep) | Q(carrier__department_2=dep) | Q(carrier__department_3=dep) | Q(carrier__department_4=dep))
        myFilter = CarrierNodeFilter(
            self.request.GET, queryset=carrier_node_queryset.order_by("is_active"))
        context = {'filter': myFilter,
                   'carrier_node_reg_result': self.request.session.pop('carrier_node_reg', None)}
        return context


def carrier_node_approval_rejection(request, pk):
    carrier_node = CarrierNode.objects.filter(id=pk).first()
    if secretarian_carrier_department_item_select_object(request.user.id, carrier_node.carrier):
        req_user = User.objects.filter(id=carrier_node.user_ptr_id).first()
        context = {'req_user': req_user,
                   'carrier_node': carrier_node}
    return render(request, "carrier_node_app_rjc.html", context)


def carrier_node_approve(request, pk):
    carrier_node = CarrierNode.objects.filter(id=pk).first()
    if secretarian_carrier_department_item_select_object(request.user.id, carrier_node.carrier):
        user = User.objects.filter(id=carrier_node.user_ptr_id).first()
        user.is_active = True
        user.save()
        request.session["carrier_node_reg"] = "User: " + \
            str(user)+" has been activated!"
    return redirect(return_url(request, carrier_node_approve_basic_list_view_url))


def carrier_node_reject(request, pk):
    carrier_node = CarrierNode.objects.filter(id=pk).first()
    if secretarian_carrier_department_item_select_object(request.user.id, carrier_node.carrier):
        user = User.objects.filter(id=carrier_node.user_ptr_id).first()
        username = user.username
        carrier = carrier_node.carrier
        carrier.delete()
        carrier_node.delete()
        user.delete()
        request.session["carrier_node_reg"] = "User: " + \
            username+" has been deleted!"
    return redirect('secretary:sec_carriers_registrations')


class ApprovalTraineePositionsListView(ListView):
    model = TraineePosition
    context_object_name = "tps"
    template_name = "sec_trainee_positions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {
            'trainee_position_message_result': self.request.session.pop('trainee_position_message', None),
            'period_message': self.request.session.pop('period_message', None)
        }
        dep = secretarian_department_select(self.request.user.id)
        trainee_positions_queryset = TraineePosition.objects.all() if dep == "ALL" else TraineePosition.objects.filter(
            carrier_assignment__department=dep)
        myFilter = TraineePositionsFilter(
            self.request.GET, queryset=trainee_positions_queryset.order_by("finalized"))
        context = {'filter': myFilter}
        return context


class SecretaryTraineePositionUpdateView(UpdateView):
    model = TraineePosition
    form_class = TraineePositionForm
    template_name = "sec_trainee_position_update.html"
    group_required = u"secretarian"

    def test_func(self, *kwargs):
        pk = self.kwargs.get('pk')
        trainee_position = TraineePosition.objects.filter(id=pk).first()
        secretarian = Secratarian.objects.get(
            user_ptr_id=self.request.user.id)
        if self.get_object().finalized == True:
            raise PermissionDenied()
        if secretarian_department_item_select_object(self.request.user.id, trainee_position.carrier_assignment):
            return True
        return False

    def get_success_url(self):
        return "/secretary/carriers/trainee_positions"


class SecretaryTraineePositionDeleteView(DeleteView):
    model = TraineePosition
    template_name = "trainee_position_delete.html"
    context_object_name = "tp"

    def get_context_data(self, **kwargs):
        carrier_assignment = self.get_object().carrier_assignment
        if secretarian_department_item_select_object(self.request.user.id, carrier_assignment):
            return super().get_context_data(**kwargs)

    def get_success_url(self):
        return "/secretary/carriers/trainee_positions"


def trainee_position_approval_rejection(request, pk):
    trainee_position = TraineePosition.objects.filter(id=pk).first()
    if secretarian_department_item_select_object(request.user.id, trainee_position.carrier_assignment):
        context = {'trainee_position': trainee_position}
    return render(request, "trainee_position_app_rjc.html", context)


def trainee_position_approve(request, pk):
    trainee_position = TraineePosition.objects.filter(id=pk).first()
    if secretarian_department_item_select_object(request.user.id, trainee_position.carrier_assignment):
        uni_department = trainee_position.carrier_assignment.department
        ca_per = CarrierAssignmentPeriod.objects.filter(
            department=uni_department).first()
        if ca_per != None:
            if ca_per.from_date <= date.today() <= ca_per.to_date:
                trainee_position.finalized = True
                trainee_position.save()
                return redirect(return_url(request, trainee_position_approve_basic_url))
            else:
                request.session['period_message'] = 'Application period not available for department: '+uni_department
                return redirect(return_url(request, trainee_position_approve_basic_url))
        else:
            request.session['period_message'] = 'Application  not found! for department: '+uni_department
            return redirect(return_url(request, trainee_position_approve_basic_url))


def carrier_node_reject(request, pk):
    carrier_node = CarrierNode.objects.filter(id=pk).first()
    user = User.objects.filter(id=carrier_node.user_ptr_id).first()
    if secretarian_department_item_select_object(request.user.id, carrier_node):
        username = user.username
        carrier = carrier_node.carrier
        carrier.delete()
        carrier_node.delete()
        user.delete()
        context = {'message': "User: "+username+" deleted!"}
    return render(request, "carrier_registrations.html", context)


class ApprovalPreferencesListView(ListView):
    model = Preference
    context_object_name = "preferences"
    template_name = "undergraduate_students_preferences.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dep = secretarian_department_select(self.request.user.id)
        preference_positions_queryset = Preference.objects.all() if dep == "ALL" else Preference.objects.filter(
            applicant__department=dep)
        myFilter = PreferencesFilter(
            self.request.GET, queryset=preference_positions_queryset.order_by("finalized"))
        context = {'filter': myFilter}
        return context


class SecretaryPreferenceDeleteView(DeleteView):
    model = Preference
    template_name = "preference_delete.html"
    context_object_name = "tp"

    def get_context_data(self, **kwargs):
        trainee = self.get_object().applicant.trainee
        if secretarian_department_item_select_object(self.request.user.id, trainee):
            return super().get_context_data(**kwargs)

    def get_success_url(self):
        return "/secretary/students/preferences"


class SecretaryPreferenceUpdateView(UpdateView):
    model = Preference
    context_object_name = "preference"
    template_name = "sec_undergraduate_preference_update.html"
    form_class = SecrataryPreferenceForm
    success_url = "/secretary/students/preferences"

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        pk = self.kwargs.get('pk')
        preference = Preference.objects.filter(id=pk).first()
        student = preference.applicant
        if secretarian_department_item_select_object(self.request.user.id, student):
            for i in range(1, 5):
                form.fields[
                    "trainee_position_" + str(i)
                ].queryset = TraineePosition.objects.filter(
                    carrier_assignment__department=student.department
                )
        return form

    def get_object(self):
        pk = self.kwargs.get('pk')
        preference = Preference.objects.filter(id=pk).first()
        student = preference.applicant
        return Preference.objects.filter(applicant=student).first()


class SecretaryTraineePositionAutocomplete(auto.Select2QuerySetView):
    def get_queryset(self):
        tr1 = self.forwarded.get("trainee_position_1", None)
        tr2 = self.forwarded.get("trainee_position_2", None)
        tr3 = self.forwarded.get("trainee_position_3", None)
        tr4 = self.forwarded.get("trainee_position_4", None)
        tr5 = self.forwarded.get("trainee_position_5", None)
        secretarian = Secratarian.objects.get(
            user_ptr_id=self.request.user.id)

        qs = TraineePosition.objects.filter(
            carrier_assignment__department=secretarian.department, finalized=True
        ).distinct('job_code').order_by()
        if tr1:
            qs = qs.exclude(id=tr1)
        if tr2:
            qs = qs.exclude(id=tr2)
        if tr3:
            qs = qs.exclude(id=tr3)
        if tr4:
            qs = qs.exclude(id=tr4)
        if tr5:
            qs = qs.exclude(id=tr5)
        if self.q:
            qs = qs.filter(
                Q(title__icontains=self.q)
                | Q(carrier_assignment__carrier__official_name__icontains=self.q)
            ).distinct('job_code').order_by()
        return qs


class SecretaryPreferenceDeleteView(DeleteView):
    model = Preference
    template_name = "preference_delete.html"
    context_object_name = "preference"

    def get_context_data(self, **kwargs):
        trainee = self.get_object().applicant
        if secretarian_department_item_select_object(self.request.user.id, trainee):
            return super().get_context_data(**kwargs)

    def get_success_url(self):
        return "/secretary/students/preferences"


def preferences_approve(request, pk):
    preference = Preference.objects.filter(id=pk).first()
    if secretarian_department_item_select_object(request.user.id, preference.applicant):
        preference.finalized = True
        preference.save()
    return redirect("secretary:sec_students_preferences")


def preference_approval_rejection(request, pk):
    preference = Preference.objects.filter(id=pk).first()
    if secretarian_department_item_select_object(request.user.id, preference.applicant):
        context = {'preference': preference}
    return render(request, "preference_app_rjc.html", context)


class AssingmentListView(ListView):
    model = Assignment
    context_object_name = "assignments"
    template_name = "sec_assignments.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dep = secretarian_department_select(self.request.user.id)
        assignments_queryset = Assignment.objects.all() if dep == "ALL" else Assignment.objects.filter(
            trainee__department=dep)
        myFilter = AssignmentFilter(
            self.request.GET, queryset=assignments_queryset.order_by(
                "finalized", "assignment_status"))
        context = {'filter': myFilter}
        return context


class AssingmentCreateView(CreateView):
    model = Assignment
    context_object_name = "assignments"
    form_class = AssignmentSecretaryForm
    template_name = "sec_create_assignment.html"
    succes_url = "/secretary/assignments"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department_request = self.request.GET.get("department")
        if secretarian_department_item_select(self.request.user, department_request):
            if department_request not in deps:
                raise Http404
            context['form'].fields['trainee'].queryset = UndergraduateStudent.objects.filter(
                department=department_request).all()
            context['form'].fields['trainee_position'].queryset = TraineePosition.objects.filter(
                carrier_assignment__department=department_request, finalized=True).all()
            context['form'].fields['supervisor'].queryset = Supervisor.objects.filter(
                department=department_request).all()
            context['form'].fields['assignment_period'].queryset = AssignmentPeriod.objects.filter(
                department=department_request).all()
        return context

    def get_success_url(self):
        department_request = self.request.GET.get("department")
        if department_request not in deps:
            raise Http404
        return "/secretary/assignments?department="+department_request

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        return form

    def form_valid(self, form):
        return super().form_valid(form)


class AssingmentUpdateView(UpdateView):
    model = Assignment
    context_object_name = "assignments"
    form_class = AssignmentSecretaryForm
    template_name = "create_assignment.html"
    succes_url = "/"

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        return form


class AssignmentDetailView(DetailView):
    model = Assignment
    context_object_name = "assignment"
    template_name = "sec_assignment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        assignment = Assignment.objects.filter(id=pk).first()
        if secretarian_department_item_select_object(self.request.user.id, assignment.trainee):
            student = assignment.trainee
            report = InternshipReport.objects.filter(
                assignment__trainee=student)
            if report.exists():
                context["report"] = report.first()
            carrier_asessment = CarrierAssesement.objects.filter(
                assignement_upon=assignment)
            if carrier_asessment.exists():
                context["carrier_assesment"] = carrier_asessment.first()
            supervisor_assesment = SupervisorAssesment.objects.filter(
                assignement_upon=assignment)
            if supervisor_assesment.exists():
                context["supervisor_assesment"] = supervisor_assesment.first()
            context["assignment"] = assignment
        return context

    def get_object(self):
        pk = self.kwargs.get('pk')
        assignment = Assignment.objects.filter(id=pk).first()
        student = assignment.trainee
        carrier_consent = CarrierConsent.objects.filter(
            assignement_upon__trainee=student, consent=True)
        if carrier_consent.exists():
            return carrier_consent.first()
        return None


class AssingmentDeleteView(DeleteView):
    model = Assignment
    context_object_name = "assignment"
    form_class = AssignmentSecretaryForm
    template_name = "sec_assignment_delete.html"
    succes_url = "/"

    def get_context_data(self, **kwargs):
        trainee = self.get_object().trainee
        if secretarian_department_item_select_object(self.request.user.id, trainee):
            return super().get_context_data(**kwargs)

    def get_success_url(self):
        return "/secretary/assignments"


def assignment_approve(request, pk):
    assignment = Assignment.objects.filter(id=pk).first()
    assignment.assingment_status = "A"
    assignment.save()
    return redirect(return_url(request, assignment_approve_basic_url))


def assignment_reject(request, pk):
    assignment = Assignment.objects.filter(id=pk).first()
    if secretarian_department_item_select_object(request.user.id, assignment.trainee):
        assignment.assingment_status = "R"
        assignment.save()
    return redirect(return_url(request, assignment_approve_basic_url))


def assignment_finalize(request, pk):
    assignment = Assignment.objects.filter(id=pk).first()
    if secretarian_department_item_select_object(request.user.id, assignment.trainee):
        assignment.finalized = True
        assignment.save()
    return redirect(assignment_approve_basic_url)


def assignment_discard(request, pk):
    assignment = Assignment.objects.filter(id=pk).first()
    if secretarian_department_item_select_object(request.user.id, assignment.trainee):
        assignment.assingment_status = "R"
    return redirect(assignment_approve_basic_url)


class InternshipReportListView(ListView):
    model = InternshipReport
    context_object_name = "internship_reports"
    template_name = "sec_internship_reports.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dep = secretarian_department_select(self.request.user.id)
        internships_report_queryset = InternshipReport.objects.all() if dep == "ALL" else InternshipReport.objects.filter(
            assignment__trainee__department=dep)
        myFilter = InternshipsReportFilter(
            self.request.GET, queryset=internships_report_queryset.order_by("finalized"))
        context = {'filter': myFilter}
        return context


class InternshipReportDetailView(DetailView):
    model = InternshipReport
    context_object_name = "internship_report"
    template_name = "sec_internship_report.html"

    def get_context_data(self, **kwargs):
        trainee = self.get_object().assignment.trainee
        if secretarian_department_item_select_object(self.request.user.id, trainee):
            return super().get_context_data(**kwargs)


def internship_report_finalize(request, pk):
    internship_report = InternshipReport.objects.filter(
        assignment__id=pk).first()
    if secretarian_department_item_select_object(request.user.id, internship_report.assignment.trainee):
        internship_report.finalized = True
        internship_report.save()
    return redirect("/secretary/assignments")


def internship_report_finalize_basic(request, pk):
    internship_report = InternshipReport.objects.filter(
        id=pk).first()
    if secretarian_department_item_select_object(request.user.id, internship_report.assignment.trainee):
        internship_report.finalized = True
        internship_report.save()
    return redirect("/secretary/assignments/intern_reports/")


def internship_report_discard(request, pk):
    internship_report = InternshipReport.objects.filter(
        assignment__id=pk).first()
    if secretarian_department_item_select_object(request.user.id, internship_report.trainee):
        internship_report.finalized = False
        internship_report.save()
    return redirect("/secretary/assignments/")


def internship_report_discard_basic(request, pk):
    internship_report = InternshipReport.objects.filter(
        id=pk).first()
    if secretarian_department_item_select_object(request.user.id, internship_report.trainee):
        internship_report.finalized = True
        internship_report.save()
    return redirect("/secretary/assignments/intern_reports/")


class CarrierAssesementListView(ListView):
    model = CarrierAssesement
    context_object_name = "carrier_assesements"
    template_name = "sec_carrier_assesements.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dep = secretarian_department_select(self.request.user.id)
        carrier_assesement_queryset = CarrierAssesement.objects.all() if dep == "ALL" else CarrierAssesement.objects.filter(
            assignement_upon__trainee__department=dep)
        myFilter = CarrierAssesmentFilter(
            self.request.GET, queryset=carrier_assesement_queryset.order_by("finalized"))
        context = {'filter': myFilter}
        return context


class CarrierAssesementDetailView(DetailView):
    model = CarrierAssesement
    context_object_name = "carrier_assesement"
    template_name = "sec_carrier_assesement.html"

    def get_context_data(self, **kwargs):
        trainee = self.get_object().assignement_upon.trainee
        if secretarian_department_item_select_object(self.request.user.id, trainee):
            return super().get_context_data(**kwargs)


def carrier_assesment_finalize(request, pk):
    carrier_assesment = CarrierAssesement.objects.filter(
        assignement_upon__id=pk).first()
    if secretarian_department_item_select_object(request.user.id, carrier_assesment.assignement_upon.trainee):
        carrier_assesment.finalized = True
        carrier_assesment.save()
    return redirect("secretary:sec_assignments")


def carrier_assesment_finalize_basic(request, pk):
    carrier_assesment = CarrierAssesement.objects.filter(
        id=pk).first()
    if secretarian_department_item_select_object(request.user.id, carrier_assesment.assignement_upon.trainee):
        carrier_assesment.finalized = True
        carrier_assesment.save()
    return redirect("secretary:sec_assignment_carrier_assesements")


def carrier_assesment_discard(request, pk):
    carrier_assesment = CarrierAssesement.objects.filter(
        assignement_upon__id=pk).first()
    if secretarian_department_item_select_object(request.user.id, carrier_assesment.assignement_upon.trainee):
        carrier_assesment.finalized = False
        carrier_assesment.save()
    return redirect("secretary:sec_assignments")


def carrier_assesment_discard_basic(request, pk):
    carrier_assesment = CarrierAssesement.objects.filter(
        id=pk).first()
    if secretarian_department_item_select_object(request.user.id, carrier_assesment.assignement_upon.trainee):
        carrier_assesment.finalized = False
        carrier_assesment.save()
    return redirect("secretary:sec_assignment_carrier_assesements")


class SupervisorAssesmentListView(ListView):
    model = SupervisorAssesment
    context_object_name = "supervisor_assesements"
    template_name = "sec_supervisor_assesements.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dep = secretarian_department_select(self.request.user.id)
        supervisor_assesement_queryset = SupervisorAssesment.objects.all() if dep == "ALL" else SupervisorAssesment.objects.filter(
            assignement_upon__trainee__department=dep)
        myFilter = SupervisorAssesmentFilter(
            self.request.GET, queryset=supervisor_assesement_queryset.order_by("finalized"))
        context = {'filter': myFilter}
        return context


class SupervisorAssesmentDetailView(DetailView):
    model = SupervisorAssesment
    context_object_name = "supervisor_assesement"
    template_name = "sec_supervisor_assesement.html"

    def get_context_data(self, **kwargs):
        trainee = self.get_object().assignement_upon.trainee
        if secretarian_department_item_select_object(self.request.user.id, trainee):
            return super().get_context_data(**kwargs)


def supervisor_assesment_finalize(request, pk):
    supervisor_assesment = SupervisorAssesment.objects.filter(
        assignement_upon__id=pk).first()
    if secretarian_department_item_select_object(request.user.id, supervisor_assesment.assignement_upon.trainee):
        supervisor_assesment.finlized = True
        supervisor_assesment.save()
    return redirect("secretary:sec_assignments")


def supervisor_assesment_finalize_basic(request, pk):
    supervisor_assesment = SupervisorAssesment.objects.filter(
        id=pk).first()
    if secretarian_department_item_select_object(request.user.id, supervisor_assesment.assignement_upon.trainee):
        supervisor_assesment.finalized = True
        supervisor_assesment.save()
    return redirect("secretary:sec_assignment_supervisor_assesements")


def supervisor_assesment_discard(request, pk):
    supervisor_assesment = SupervisorAssesment.objects.filter(
        assignment_upon__id=pk).first()
    if secretarian_department_item_select_object(request.user.id, supervisor_assesment.assignement_upon.trainee):
        supervisor_assesment.finlized = False
        supervisor_assesment.save()
    return redirect("secretary:sec_assignments")


def supervisor_assesment_discard_basic(request, pk):
    supervisor_assesment = SupervisorAssesment.objects.filter(
        id=pk).first()
    if secretarian_department_item_select_object(request.user.id, supervisor_assesment.assignement_upon.trainee):
        supervisor_assesment.finalized = True
        supervisor_assesment.save()
    return redirect("/secretary/assignments/supervisor_assesments/")
