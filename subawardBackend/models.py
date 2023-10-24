from django.conf import settings
from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from .managers import CustomUserManager

import uuid

from subawardBackend.enumDec import register_enum


class AgreementStatus(models.TextChoices):
    PendingPreAward = 'Pending preaward',
    PendingNoa = 'Pending NoA',
    PendingPIDA = 'Pending PI/DA',
    PendingASetUp = 'Pending award set up',
    PendingDocSubrecp = 'Pending documents from Subrecipient',
    PendingPostAward = 'Pending post Award',
    PendingPO = 'Pending PO',
    PendingAssessments = 'Pending Assessments',
    DeterminedCFS = 'Determined to be CFS',
    OpenPending = 'Open Pending',
    Billing = 'Billing',
    Preaward = 'Preaward',
    Active = 'Active',
    Closed = 'Closed',
    Withdrawn = 'Withdrawn'


class SponsorType(models.TextChoices):
    Federal = 'Federal',
    NonFederal = 'NonFederal'


class AwardType(models.TextChoices):
    Cost = 'Cost',
    Fixed = 'Fixed'


class BillingTerms(models.TextChoices):
    Monthly = 'Monthly',
    Quaterly = 'Quaterly',
    Deliverable = 'Deliverable',


class SubagreementTracking(models.Model):
    SATAmendmentId = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    ParentAmendmentId = models.UUIDField(null=True)
    ParentRecord = models.BooleanField(null=False)
    FCDAmendmentId = models.ForeignKey(
        'FinancialCompliance', null=True, on_delete=models.CASCADE)
    PrimeAgreementExecutionDate = models.DateField(null=False)
    SubrecipientName = models.TextField(null=False)
    UEI = models.TextField(null=False)
    SAMEntity = models.BooleanField(null=False)
    SAMPI = models.BooleanField(null=False)
    # Subrecipient vs Contractor Checklist completed or not
    SubawardOrContract = models.BooleanField(null=False)
    DateOfSubawardExecution = models.DateField(null=False)
    Status = models.CharField(choices=AgreementStatus.choices,
                              null=False, default=AgreementStatus.PendingPreAward)
    SubawardNumber = models.TextField(null=False)
    PrimeAwardNumber = models.TextField(null=False)
    ProjectId = models.TextField(null=False)
    PSVendorId = models.TextField(null=False)
    PIFirstName = models.TextField(null=False)
    PILastName = models.TextField(null=False)
    PrimeSponsor = models.TextField(null=False)
    FFATA = models.BooleanField(null=False)
    IncrementallyEstimatedTotal = models.DecimalField(
        max_digits=12, decimal_places=2, null=False)
    PeriodOfPerformanceStart = models.DateField(null=False)
    PeriodOfPerformanceEnd = models.DateField(null=False)
    EstimatedPeriodOfPerformanceStart = models.DateField(null=False)
    EstimatedPeriodOfPerformanceEnd = models.DateField(null=False)
    Budget = models.BooleanField(null=False)
    Attachment3B = models.BooleanField(null=False)
    BudgetJustificationScore = models.IntegerField(null=False)
    EntityRiskAssessmentScore = models.IntegerField(null=False)
    ProjectRiskAssessmentScore = models.IntegerField(null=False)
    TwentyFiveKObligation = models.BooleanField(null=False)
    DocusignRouting = ArrayField(models.EmailField(max_length=254))
    Comments = models.TextField(null=False)
    created = models.DateTimeField(null=False, auto_now_add=True)

    def get_agreement_status(self) -> AgreementStatus:
        return AgreementStatus[self.Status]

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(PeriodOfPerformanceStart__lte=models.F(
                    'PeriodOfPerformanceEnd')),
                name='PeriodOfPerfstart_lt_PeriodOfPerfEnd'
            ),
            models.CheckConstraint(
                check=models.Q(EstimatedPeriodOfPerformanceStart__lte=models.F(
                    'EstimatedPeriodOfPerformanceEnd')),
                name='EtdPeriodOfPerfst_lt_EtdPeriodOfPerfEnd'
            ),
            # ParentAmendmentId
            # ParentRecord
            models.CheckConstraint(
                check=models.Q(ParentAmendmentId__isnull=True, ParentRecord=True) | models.Q(
                    ParentAmendmentId__isnull=False, ParentRecord=False),
                name="ParentAmendmentIsNullforParentRecord"
            ),
        ]


class FinancialCompliance(models.Model):
    FCDAmendmentId = models.UUIDField(
        null=False, primary_key=True, default=uuid.uuid4, editable=False)
    # prefill this with subaward name, PI Name, Prime Sponsor
    ParentAmendmentId = models.UUIDField(null=True)
    ParentRecord = models.BooleanField(null=False)
    # Note: Replace on_delete cascade with something else
    SATAmendmentId = models.ForeignKey(
        'SubagreementTracking', null=True, on_delete=models.CASCADE)
    POnumber = models.TextField(null=True)
    DateFinalInvoiceRecieved = models.DateField(null=True)
    DateFinalInvoiceDue = models.DateField(null=True)
    PrimeSponsorType = models.CharField(
        max_length=255, choices=SponsorType.choices, null=True, blank=True)
    AwardType = models.CharField(
        max_length=255, choices=AwardType.choices, null=True, blank=True)
    BillingTerms = models.CharField(
        max_length=255, choices=BillingTerms.choices, null=True, blank=True)
    # is not null only id another table has FFATA
    FFATAFilledDate = models.DateField(null=True)
    Notes = models.TextField()
    created = models.DateTimeField(null=False, auto_now_add=True)

    def save(self, *args, **kwargs):
        # Set fields to None if they are empty strings (e.g., "")
        if self.PrimeSponsorType == "":
            self.PrimeSponsorType = None
        if self.AwardType == "":
            self.AwardType = None
        if self.BillingTerms == "":
            self.BillingTerms = None

        super().save(*args, **kwargs)


# class Subawards(models.Model):
#     SbAId = models.UUIDField(null=False, primary_key=True,
#                              default=uuid.uuid4, editable=False)
#     SATAmmendmentId = models.ForeignKey(
#         SubagreementTracking, on_delete=models.CASCADE)
#     # Note: Replace on_delete cascade with something else
#     FCDAmmendmentId = models.ForeignKey(
#         FinancialCompliance, on_delete=models.CASCADE)
#     # Note: Replace on_delete cascade with something else


class CustomUser(AbstractUser):
    EMPLOYEE_TYPE = (
        ('student_employee', 'student employee'),
        ('permanent_employee', 'permanent employee'),
        ('temporary_employee', 'temporary employee'),
    )
    email = models.EmailField(unique=True)
    employee_type = models.CharField(
        max_length=100, choices=EMPLOYEE_TYPE, default='regular')

    objects = CustomUserManager()

    def __str__(self):
        return self.username


'''
Financial Compliance
    FCDAmmendmentId
    POnumber
    SubsiteName (present in new screen and pre filled maybe related to the subrecipient Agreement tracking)
    PIName
    FinalInvoiceDueDate
    DateFinalInvoiceRecieved
    PrimeSponsor
    AwardType
    BillingTerms
    FFATAFilledDate BOOLEAN (only active if there in previous table)
    Notes
'''

'''
    Subrecipient Agreement Tracking 

    SATAmmendmentId UUID PRIMARY KEY,
    PrimeAgreementExecutionDate DATE NOT NULL,
    SubrecipientName TEXT NOT NULL,
    UEI TEXT NOT NULL,
    SAMEntity BOOLEAN NOT NULL,
    SAMPI BOOLEAN NOT NULL,
    SubawardOrContract BOOLEAN NOT NULL, //IF yes then SubAward else SubawardOrContract
    DateOfExecution DATE NOT NULL,
    Status AgreementStatus NOT NULL,
    SubAwardNumber TEXT,
    AwardNumber TEXT,
    ProjectID TEXT NOT NULL,
    PSVendorID TEXT NOT NULL,
    PIFirstName TEXT NOT NULL,
    PILastName TEXT NOT NULL,
    PrimeSponsor SponsorType NOT NULL,
    FFATA BOOLEAN NOT NULL,
    IncrementallyEstimatedTotal DECIMAL(12,2) NOT NULL,
    PeriodOfPerformanceStart DATE NOT NULL,
    PeriodOfPerformanceEnd DATE NOT NULL,
    EstimatedPeriodOfPerformanceStart DATE NOT NULL,
    EstimatedPeriodOfPerformanceEnd DATE NOT NULL,
    Budget BOOLEAN NOT NULL,
    Attachment3B BOOLEAN NOT NULL,
    BudgetJustification BOOLEAN NOT NULL,
    EntityRiskAssessment BOOLEAN NOT NULL,
    ProjectRiskAssessment BOOLEAN NOT NULL,
    25KObligation BOOLEAN NOT NULL,
    DocusignRouting (WIP)
    Comments TEXT

    SponsorType ENUM (
        "Federal",
        "Non-Federal"
    )

    AgreementStatus ENUM (
        "Pending NoA",
        "Pending PI/DA",
        "Pending award set up",
        "Pending documents from Subrecipient",
        "Pending post Award",
        "Determined to be CFS",
        "Active",
        "Closed",
        "Withdrawn",
    )
    AwardType ENUM (
        COST,
        FIXED
    )

    BillingTerms ENUM (
        Monthly,
        Quaterly,
        Deliverable
    )

    Subawards
    SbAId UUID PRIMARY KEY
    SATAmmendmentId UUID NOT NULL UNIQUE
    FCDAmmendmentId UUID NOT NULL UNIQUE



    Financial Compliance
    FCDAmmendmentId
    POnumber
    SubsiteName (present in new screen and pre filled maybe related to the subrecipient Agreement tracking)
    PIName
    FinalInvoiceDueDate
    DateFinalInvoiceRecieved
    PrimeSponsor
    AwardType
    FFATAFilledDate BOOLEAN (only active if there in previous table)
    Notes

'''

'''

Note down constrains:
1. 

'''
