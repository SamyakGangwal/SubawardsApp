from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from subawardBackend.forms import CustomUserCreationForm, SubagreementTrackingForm, FinancialComplianceForm
from django.contrib.auth.decorators import login_required
from subawardBackend.model_functions import create_financial_compliance_record, create_subaward_record
from subawardBackend.models import FinancialCompliance
from subawardBackend.models import Subawards
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


@login_required
def subaward_request_tracking(request):
    if request.method == 'POST':
        form = SubagreementTrackingForm(request.POST)
        if form.is_valid():
            subagreementrecord = form.save()
            financial_compliance_record = create_financial_compliance_record(
                subagreementrecord)
            create_subaward_record(
                subagreementrecord, financial_compliance_record)
            return redirect('dashboard')
        else:
            # Display form errors using messages framework
            for field, error in form.errors.items():
                messages.error(request, f"Error in {field}: {error}")
    else:
        form = SubagreementTrackingForm()
    return render(request, "subawardRequestTracking.html", {'form': form})


@login_required
def financial_compliance_dashboard(request, amendment_id):
    record = get_object_or_404(
        FinancialCompliance, FCDAmmendmentId=amendment_id)

    if request.method == 'POST':
        form = FinancialComplianceForm(request.POST)
        if form.is_valid():
            # Process the form data, e.g., save it to the database
            form.save()
            return redirect('dashboard')
        else:
            for field, error in form.errors.items():
                print(request, f"Error in {field}: {error}")
    else:
        form = FinancialComplianceForm()

    return render(request, 'financialCompliance.html', {'form': form, 'record': record})


@login_required
def list_records(request):
    # join 2 tables
    # subrecipient name, PI first name + PI last Name, Prime Sponsor
    subawardT_data = SubagreementTracking.objects.all()

    financialcompT_data = FinancialCompliance.objects.all()
    # fin_cmp = FinancialCompliance.objects.select_related("SATAmmendmentId")
    subaward_records = Subawards.objects.all()

    # Define the Eastern Time (ET) timezone
    eastern_timezone = pytz.timezone('US/Eastern')

    for subawardR in subawardT_data:
        subawardR.created = subawardR.created.isoformat()

    for financialC in financialcompT_data:
        financialC.created = financialC.created.isoformat()

    return render(request, 'listRecords.html', {'subawardT': subawardT_data, 'subaward_records': subaward_records, 'financialComp': financialcompT_data})


@login_required
def subaward_detail(request, amendment_id):
    record = get_object_or_404(
        SubagreementTracking, SATAmmendmentId=amendment_id)

    if request.method == 'POST':
        form = SubagreementTrackingForm(request.POST)
        if form.is_valid():
            subagreementrecord = form.save()
            financial_compliance_record = create_financial_compliance_record(
                subagreementrecord)
            create_subaward_record(
                subagreementrecord, financial_compliance_record)
            return redirect('dashboard')
        else:
            # Display form errors using messages framework
            for field, error in form.errors.items():
                print(request, f"Error in {field}: {error}")

    return render(request, 'subawardDetails.html', {'record': record})
