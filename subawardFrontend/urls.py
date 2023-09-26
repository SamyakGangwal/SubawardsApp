from django.urls import path
from .views import signup, dashboard, subaward_request_tracking, financial_compliance_dashboard, list_records, subaward_detail

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("", dashboard, name="dashboard"),
    path("subaward-request-tracking", subaward_request_tracking,
         name="subaward_request_tracking"),
    path('financial-compliance/<str:amendment_id>/', financial_compliance_dashboard,
         name='financial_compliance_dashboard'),
    path('list-records/', list_records, name='list_records'),
    path('subawards/<str:amendment_id>/', subaward_detail, name='subaward_detail')
]
