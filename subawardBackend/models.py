from django.conf import settings
from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from .managers import CustomUserManager

import uuid

from subawardBackend.enumDec import register_enum


class AgreementStatus(models.TextChoices):
    PendingPreAward = 'Pending preaward',
    PendingNoa = 'Pending NoA',
    PendingPIDA = 'Pending PI/DA',
    PendingDocSubrecp = 'Pending documents from Subrecipient',
    PendingPostAward = 'Pending post Award',
    PendingPO = 'Pending PO',
    PendingAssessments = 'Pending Assessments',
    DeterminedCFS = 'Determined to be CFS',
    OpenPending = 'Open Pending',
    Executed = 'Executed',
    Preaward = 'Preaward',
    Active = 'Active',
    Closed = 'Closed',
    Withdrawn = 'Withdrawn'

class USMCRiskTypes(models.TextChoices):
    Low = 'Low',
    Medium = 'Medium',
    High = 'High'

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
    OverallRiskAssessmentScore = models.IntegerField(null=False)
    USMCRiskDetermination = models.CharField(choices=USMCRiskTypes.choices,
                              null=False)
    TwentyFiveKObligation = models.BooleanField(null=False)
    DocusignRouting = ArrayField(models.EmailField(max_length=254))
    Comments = models.TextField(null=True)
    created = models.DateTimeField(null=False, auto_now_add=True)

    def get_USMCRiskType(self) -> USMCRiskTypes:
        return USMCRiskTypes[self.USMCRiskDetermination]

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


# TODO: update this such that I am able to add the correct user type, and , umb email sign up with OTP and all and then single sign on
class CustomUser(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=300, blank=False)
    last_name = models.CharField(max_length=300, blank=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    date_joined = models.DateField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD= 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name = 'Users'

    def get_full_name(self):
        return self.first_name + " " + self.last_name
    
    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.username
    
    @property
    def is_staff(self):
        return self.is_staff
