from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from subawardBackend.forms import CustomUserCreationForm, SubagreementTrackingForm, FinancialComplianceForm
from subawardBackend.model_functions import create_empty_financial_compliance_record
from subawardBackend.models import FinancialCompliance
from subawardBackend.models import SubagreementTracking

import pytz
from datetime import datetime


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in.
            login(request, user)
            # Redirect to the home page after successful signup
            return redirect('dashboard')
        else:
            print(form.errors)  # Print form errors for troubleshooting
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def dashboard(request):
    return render(request, "subawardsHome.html")


# create subaward request
@login_required
def create_subaward_request_tracking(request):
    if request.method == 'POST':
        form = SubagreementTrackingForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    subagreementrecord = form.save(commit=False)
                    subagreementrecord.ParentRecord = True
                    subagreementrecord.save()

                    financial_compliance_record = create_empty_financial_compliance_record(
                        subagreementrecord, True)

                    subagreementrecord.FCDAmendmentId = financial_compliance_record
                    financial_compliance_record.SATAmendmentId = subagreementrecord
                    subagreementrecord.save()
                    financial_compliance_record.save()

                    return redirect('dashboard')
            except Exception as e:
                # Handle the exception or show an error message
                transaction.set_rollback(True)  # Rollback the transaction
                messages.error(request, f"Error: {str(e)}")
        else:
            # Display form errors using messages framework
            for field, error in form.errors.items():
                messages.error(request, f"Error in {field}: {error}")
    else:
        form = SubagreementTrackingForm()
    return render(request, "createSubawardRequestTracking.html", {'form': form})

# @login_required
# def update_subaward_request_tracking(request, amendment_id):
#     if request.method == 'POST':
#         form = SubagreementTrackingForm(request.POST)
#     # Update the latest financial compliance with the subagreement ID
#     #
#         if form.is_valid():
#             subagreementrecord = form.save(commit=False)
#             subagreementrecord.ParentRecord = True
#             subagreementrecord.save()

#             financial_compliance_record = create_empty_financial_compliance_record(
#                 subagreementrecord, True)

#             subagreementrecord.FCDAmendmentId = financial_compliance_record
#             financial_compliance_record.SATAmendmentId = subagreementrecord
#             subagreementrecord.save()
#             financial_compliance_record.save()

#             return redirect('dashboard')


# @login_required
# def financial_compliance_dashboard(request, amendment_id):
#     record = get_object_or_404(
#         FinancialCompliance, FCDAmendmentId=amendment_id)

#     if request.method == 'POST':
#         form = FinancialComplianceForm(
#             amendment_id=amendment_id, data=request.POST)

#         if form.is_valid():
#             form.save()
#             return redirect('dashboard')
#         else:
#             for field, error in form.errors.items():
#                 print(request, f"Error in {field}: {error}")
#     else:
#         form = FinancialComplianceForm(amendment_id=amendment_id)

#     return render(request, 'financialCompliance.html', {'form': form, 'record': record})


@login_required
def list_base_records(request):
    # join 2 tables
    # subrecipient name, PI first name + PI last Name, Prime Sponsor
    subawardT_data = SubagreementTracking.objects.filter(
        ParentRecord=True).select_related('FCDAmendmentId')

    financialcompT_data = FinancialCompliance.objects.filter(
        ParentRecord=True).select_related('SATAmendmentId')

    childRecordS = []
    childRecordF = []
    for record in subawardT_data:
        if len(SubagreementTracking.objects.filter(ParentAmendmentId=record.SATAmendmentId).values_list()) == 0:
            childRecordS.append(False)
        else:
            childRecordS.append(True)

    for record in financialcompT_data:
        if len(FinancialCompliance.objects.filter(ParentAmendmentId=record.FCDAmendmentId).values_list()) == 0:
            childRecordF.append(False)
        else:
            childRecordF.append(True)
    # fin_cmp = FinancialCompliance.objects.select_related("SATAmmendmentId")
    # subaward_records = Subawards.objects.all()

    # Define the Eastern Time (ET) timezone
    eastern_timezone = pytz.timezone('US/Eastern')

    for subawardR in subawardT_data:
        subawardR.created = subawardR.created.isoformat()

    for financialC in financialcompT_data:
        financialC.created = financialC.created.isoformat()

    return render(request, 'listParentRecords.html', {'subawardT': zip(subawardT_data, childRecordS), 'financialComp': zip(financialcompT_data, childRecordF)})


@login_required
def list_subagreement_child_records(request, amendment_id):
    # join 2 tables
    # subrecipient name, PI first name + PI last Name, Prime Sponsor

    subawardT_data = SubagreementTracking.objects.filter(
        ParentRecord=False, ParentAmendmentId=amendment_id).select_related('FCDAmendmentId')

    latestChild = SubagreementTracking.objects.filter(
        ParentAmendmentId=amendment_id).select_related('FCDAmendmentId').order_by('-created').first()

    # Define the Eastern Time (ET) timezone
    eastern_timezone = pytz.timezone('US/Eastern')

    for subawardR in subawardT_data:
        subawardR.created = subawardR.created.isoformat()

    return render(request, 'listSubagreementChildRecords.html', {'subawardT': subawardT_data, 'parentAmendmentId': amendment_id, 'child': latestChild})


@login_required
def list_financial_compliance_child_records(request, amendment_id):
    # join 2 tables
    # subrecipient name, PI first name + PI last Name, Prime Sponsor

    financialcompT_data = FinancialCompliance.objects.filter(
        ParentRecord=False, ParentAmendmentId=amendment_id).select_related('SATAmendmentId')
    # fin_cmp = FinancialCompliance.objects.select_related("SATAmmendmentId")
    # subaward_records = Subawards.objects.all()

    latestChild = FinancialCompliance.objects.filter(
        ParentAmendmentId=amendment_id).select_related('SATAmendmentId').order_by('-created').first()

    # Define the Eastern Time (ET) timezone
    eastern_timezone = pytz.timezone('US/Eastern')

    for financialC in financialcompT_data:
        financialC.created = financialC.created.isoformat()

    return render(request, 'listFinancialComplianceChildRecords.html', {'financialComp': financialcompT_data, 'parentAmendmentId': amendment_id, 'child': latestChild})


@login_required
def update_subaward_request_tracking(request, amendment_id):
    record = get_object_or_404(
        SubagreementTracking, SATAmendmentId=amendment_id)

    if request.method == 'POST':
        form = SubagreementTrackingForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():    
                    subagreementrecord = form.save(commit=False)
                    subagreementrecord.ParentRecord = False
                    if record.ParentRecord:
                        subagreementrecord.ParentAmendmentId = amendment_id
                    else:
                        subagreementrecord.ParentAmendmentId = record.ParentAmendmentId
                    subagreementrecord.FCDAmendmentId = record.FCDAmendmentId
                    subagreementrecord.save()
                    fcda_record = get_object_or_404(
                        FinancialCompliance, FCDAmendmentId=record.FCDAmendmentId.FCDAmendmentId)
                    fcda_record.SATAmendmentId = subagreementrecord
                    fcda_record.save()

                    return redirect('dashboard')
            except Exception as e:
                # Handle the exception or show an error message
                transaction.set_rollback(True)  # Rollback the transaction
                messages.error(request, f"Error: {str(e)}")
        else:
            # Display form errors using messages framework
            for field, error in form.errors.items():
                messages.error(request, f"Error in {field}: {error}")

    record.DocusignRouting = ','.join(record.DocusignRouting)

    return render(request, 'subawardDetails.html', {'record': record, })


@login_required
def update_financial_compliance(request, amendment_id):
    record = get_object_or_404(
        FinancialCompliance, FCDAmendmentId=amendment_id)

    if request.method == 'POST':
        form = FinancialComplianceForm(request.POST, amendment_id=amendment_id)
        if form.is_valid():
            try:
                with transaction.atomic():
                    financial_compliance_record = form.save(commit=False)
                    financial_compliance_record.ParentRecord = False
                    if record.ParentRecord:
                        financial_compliance_record.ParentAmendmentId = amendment_id
                    else:
                        financial_compliance_record.ParentAmendmentId = record.ParentAmendmentId
                    financial_compliance_record.SATAmendmentId = record.SATAmendmentId
                    financial_compliance_record.save()

                    subawd_record = get_object_or_404(
                        SubagreementTracking, SATAmendmentId=record.SATAmendmentId.SATAmendmentId)
                    subawd_record.FCDAmendmentId = financial_compliance_record
                    subawd_record.save()

                    return redirect('dashboard')
            except Exception as e:
                # Handle the exception or show an error message
                transaction.set_rollback(True)  # Rollback the transaction
                messages.error(request, f"Error: {str(e)}")
        else:
            # Display form errors using messages framework
            for field, error in form.errors.items():
                print(request, f"Error in {field}: {error}")

    return render(request, 'financialCompliance.html', {'record': record})

@login_required
def view_subaward_details(request, amendment_id):
    record = get_object_or_404(
        SubagreementTracking, SATAmendmentId=amendment_id)

    record.DocusignRouting = ','.join(record.DocusignRouting)

    return render(request, 'viewSubawardDetails.html', {'record': record})

@login_required
def view_financial_compliance(request, amendment_id):
    record = get_object_or_404(
        FinancialCompliance, FCDAmendmentId=amendment_id)

    return render(request, 'viewFinancialCompliance.html', {'record': record})

'''
Now create a new view where when a person clicks on create a new amendment 
it pulls the latest amendment and then let's the user update it.

'''


# @login_required
# def create_subaward_amendment(request, amendment_id):
# record = SubagreementTracking.objects.filter(
#     ParentAmendmentId=amendment_id).select_related('FCDAmendmentId').order_by('-created').first()

#     print(record)

#     if record is None:
#         base_record = get_object_or_404(
#             SubagreementTracking, SATAmendmentId=amendment_id)
#         return render(request, 'subawardDetails.html', {'record': base_record, 'parentAmendmentId': amendment_id})

#     return render(request, 'subawardDetails.html', {'record': record, 'parentAmendmentId': amendment_id})
