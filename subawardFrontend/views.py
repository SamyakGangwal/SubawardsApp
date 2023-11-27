import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from subawardBackend.forms import CustomUserCreationForm, SubagreementTrackingForm, FinancialComplianceForm
from subawardBackend.model_functions import create_empty_financial_compliance_record
from subawardBackend.models import FinancialCompliance
from subawardBackend.models import SubagreementTracking
from subawardBackend.tokens import account_activation_token

import pytz
from datetime import datetime

# Create a logger for this file
logger = logging.getLogger(__file__)

# TODO: add try catch and return errors if any
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    # Log the user in.
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    # Redirect to the home page after successful signup
                    return redirect('dashboard')
                    # return redirect('verify-email')
            except Exception as e:
                # Handle the exception or show an error message
                transaction.set_rollback(True)  # Rollback the transaction
        else:
            # Display form errors using messages framework
            for field, error in form.errors.items():
                logger.error(f"Error in {field}: {error}")

            errors = {field: error[0] for field, error in form.errors.items()}

            response_data = {'errors': errors}
            return JsonResponse(response_data, status=400)
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# TODO: add login function through try catch and return error if any

# send email with verification link
# def verify_email(request):
#     if request.method == "POST":
#         if request.user.email_is_verified != True:
#             current_site = get_current_site(request)
#             user = request.user
#             email = request.user.email
#             subject = "Verify Email"
#             message = render_to_string('user/verify_email_message.html', {
#                 'request': request,
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token':account_activation_token.make_token(user),
#             })
#             email = EmailMessage(
#                 subject, message, to=[email]
#             )
#             email.content_subtype = 'html'
#             email.send()
#             return redirect('verify-email-done')
#         else:
#             return redirect('signup')
#     return render(request, 'user/verify_email.html')


def dashboard(request):  
    return render(request, "subawardsHome.html")

# def verify_email_done(request):
#     return render(request, 'users/verify_email_done.html')

# def verify_email_confirm(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.email_is_verified = True
#         user.save()
#         messages.success(request, 'Your email has been verified.')
#         return redirect('verify-email-complete')   
#     else:
#         messages.warning(request, 'The link is invalid.')
#     return render(request, 'user/verify_email_confirm.html')

# def verify_email_complete(request):
#     return render(request, 'user/verify_email_complete.html')

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
        else:
            # Display form errors using messages framework
            for field, error in form.errors.items():
                logger.error(f"Error in {field}: {error}")

            errors = {field: error[0] for field, error in form.errors.items()}

            response_data = {'errors': errors}
            return JsonResponse(response_data, status=400)
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
