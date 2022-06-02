from .models import ApplicationPeriod, AssignmentPeriod, CarrierAssignmentPeriod, InternshipReportPeriod

def check_periods(uni_department):
    app_period = ApplicationPeriod.objects.filter(
            department=uni_department
        ).first()
    assignment_period = AssignmentPeriod.objects.filter(
            department=uni_department
        ).first()
    carrier_assignment_period = CarrierAssignmentPeriod.objects.filter(
            department=uni_department
        ).first()
    internship_report_period = InternshipReportPeriod.objects.filter(
        department=uni_department
    )
    validation_message=""
    if app_period and carrier_assignment_period:
        if carrier_assignment_period.to_date  > app_period.from_date:
            validation_message = validation_message+"\n"+"Periods conflict on Department "+uni_department+" starting date of Application Period: "+str(app_period.from_date)+" and ending date for carrier assignments: "+str(carrier_assignment_period.to_date)
    if assignment_period and app_period:
        if app_period.to_date  > assignment_period.from_date:
            validation_message = validation_message+"\n"+"Periods conflict on Department "+uni_department+" starting date of Assignment Period: "+str(assignment_period.from_date)+" and ending date for applications: "+str(app_period.to_date)
    if carrier_assignment_period and assignment_period:
        if carrier_assignment_period.to_date  > assignment_period.from_date:
            validation_message = validation_message+"\n"+"Periods conflict on Department "+uni_department+" starting date of Assignment Period: "+str(assignment_period.from_date)+" and ending date for carrier assignments: "+str(carrier_assignment_period.to_date)
    if assignment_period and internship_report_period:
        if assignment_period.to_date > internship_report_period.from_date:
            validation_message = validation_message+"\n"+"Periods conflict on Department "+uni_department+" starting date of Internship Report Period: "+str(internship_report_period.from_date)+" and ending date for Assignment: "+str(assignment_period.to_date)
    if app_period and internship_report_period:
        if app_period.to_date > internship_report_period.from_date:
            validation_message = validation_message+"\n"+"Periods conflict on Department "+uni_department+" starting date of Internship Report Period: "+str(internship_report_period.from_date)+" and ending date for applications: "+str(app_period.to_date)
    if carrier_assignment_period and internship_report_period:
        if carrier_assignment_period.to_date > internship_report_period.from_date:
            validation_message = validation_message+"\n"+"Periods conflict on Department "+uni_department+" starting date of Internship Report Period: "+str(internship_report_period.from_date)+" and ending date for carreir assignments: "+str(carrier_assignment_period.to_date)
    if validation_message !="":
        return validation_message
    return True