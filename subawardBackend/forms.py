from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import CustomUser, SponsorType, AwardType, AgreementStatus, SubagreementTracking, FinancialCompliance


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields  # Include any additional fields if needed


class SubagreementTrackingForm(ModelForm):
    class Meta:
        model = SubagreementTracking
        fields = ["PrimeAgreementExecutionDate",
                  "SubrecipientName",
                  "UEI",
                  "SAMEntity",
                  "SAMPI",
                  "SubawardOrContract",
                  "DateOfSubawardExecution",
                  "Status",
                  "SubawardNumber",
                  "PrimeAwardNumber",
                  "ProjectId",
                  "PSVendorId",
                  "PIFirstName",
                  "PILastName",
                  "PrimeSponsor",
                  "FFATA",
                  "IncrementallyEstimatedTotal",
                  "PeriodOfPerformanceStart",
                  "PeriodOfPerformanceEnd",
                  "EstimatedPeriodOfPerformanceStart",
                  "EstimatedPeriodOfPerformanceEnd",
                  "Budget",
                  "Attachment3B",
                  "BudgetJustificationScore",
                  "EntityRiskAssessmentScore",
                  "ProjectRiskAssessmentScore",
                  "TwentyFiveKObligation",
                  "DocusignRouting",
                  "Comments",
                  ]

class FinancialComplianceForm(ModelForm):
    class Meta:
        model = FinancialCompliance
        fields = [
            "POnumber", 
            "SATAmmendmentId", 
            "DateFinalInvoiceRecieved", 
            "PrimeSponsorType", 
            "AwardType", 
            "BillingTerms", 
            "FFATAFilledDate", 
            "Notes"
            ]