from django.contrib import admin

# Register your models here.
from .models import AgreementStatus
from .models import SponsorType
from .models import AwardType
from .models import BillingTerms
from .models import SubagreementTracking
from .models import FinancialCompliance
from .models import CustomUser

# admin.site.register(AgreementStatus)
# admin.site.register(SponsorType)
# admin.site.register(AwardType)
# admin.site.register(BillingTerms)
admin.site.register(SubagreementTracking)
admin.site.register(FinancialCompliance)
admin.site.register(CustomUser)