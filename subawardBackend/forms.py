from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, ValidationError
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
            "DateFinalInvoiceRecieved",
            "DateFinalInvoiceDue",
            "PrimeSponsorType",
            "AwardType",
            "BillingTerms",
            "FFATAFilledDate",
            "Notes"
        ]

    def __init__(self, *args, **kwargs):
        self.FCDAmendmentId = kwargs.pop('amendment_id')
        super(FinancialComplianceForm, self).__init__(*args, **kwargs)
        self.fields['POnumber'].required = False
        self.fields['DateFinalInvoiceRecieved'].required = False
        self.fields['DateFinalInvoiceDue'].required = False
        self.fields['PrimeSponsorType'].required = False
        self.fields['AwardType'].required = False
        self.fields['BillingTerms'].required = False
        self.fields['FFATAFilledDate'].required = False
        self.fields['Notes'].required = False

    def clean(self):
        f_data = self.cleaned_data

        financialCompliance_rec = FinancialCompliance.objects.filter(
            FCDAmendmentId=self.FCDAmendmentId).first()

        if (financialCompliance_rec.SATAmendmentId.FFATA == False and 'FFATAFilledDate' not in f_data):
            raise ValidationError(
                "The preaward process indicated that this is not a Federally funded project")

        return f_data
