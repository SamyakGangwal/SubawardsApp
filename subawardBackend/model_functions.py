from subawardBackend.forms import SubagreementTrackingForm
from subawardBackend.models import FinancialCompliance
from subawardBackend.models import Subawards

def create_financial_compliance_record(subagreementrecord):
    fc_record = FinancialCompliance(SATAmmendmentId=subagreementrecord)
    fc_record.save()
    return fc_record

def create_subaward_record(subagreementrecord, fc_record):
    subaward_record = Subawards()
    subaward_record.SATAmmendmentId = subagreementrecord
    subaward_record.FCDAmmendmentId = fc_record
    subaward_record.save()
    return subaward_record

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