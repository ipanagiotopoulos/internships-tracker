from django.urls import path
from . import views

app_name = "applicant"

urlpatterns = [
    path(
        "application/update",
        views.PreferenceUpdateView.as_view(),
        name="student_preference_update",
    ),
    path(
        "application/my",
        views.PreferenceDetailView.as_view(),
        name="student_preference_detail",
    ),
    path(
        "application/submit",
        views.CreatePreferenceView.as_view(),
        name="student_preference_submit",
    ),
    path(
        "positions",
        views.TraineePositionStudentListView.as_view(),
        name="student_all_positions",
    ),
    path(
        "my-carrier-consent",
        views.MyCarrierConsentDetailView.as_view(),
        name="my_carrier_consent",
    ),
    path(
        "my-carrier-consent/<int:pk>/upload-report",
        views.InternshipReportCreateView.as_view(),
        name="report_create",
    ),
    path(
        "my-carrier-consent/<int:pk>/update-report/<int:report_id>",
        views.InternshipReportUpdateView.as_view(),
        name="report_update",
    ),
    path(
        "application-period/not-found",
        views.application_period_not_found,
        name="application_period_not_found",
    ),
    path(
        "report-period/not-found",
        views.report_period_not_found,
        name="report_period_not_found",
    ),
]
