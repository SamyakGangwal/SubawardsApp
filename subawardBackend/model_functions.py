from subawardBackend.forms import SubagreementTrackingForm
from subawardBackend.models import FinancialCompliance

def create_empty_financial_compliance_record(subagreementrecord, ParentRecord):
    fc_record = FinancialCompliance(SATAmendmentId=subagreementrecord, ParentRecord=ParentRecord)
    fc_record.save()
    return fc_record

'''
FCDAmmendmentId = models.UUIDField(
        null=False, primary_key=True, default=uuid.uuid4, editable=False)
    POnumber = models.TextField(null=False)
    # prefill this with subaward name, PI Name, Prime Sponsor
    SATAmmendmentId = models.ForeignKey(
        SubagreementTracking, null=False, on_delete=models.CASCADE)
    # Note: Replace on_delete cascade with something else
    DateFinalInvoiceRecieved = models.DateField(null=False)
    PrimeSponsorType = models.CharField(
        max_length=255, choices=SponsorType.choices, null=False)
    AwardType = models.CharField(
        max_length=255, choices=AwardType.choices, null=False)
    BillingTerms = models.CharField(
        max_length=255, choices=BillingTerms.choices, null=False)
    # is not null only id another table has FFATA
    FFATAFilledDate = models.BooleanField()
    Notes = models.TextField()


'''