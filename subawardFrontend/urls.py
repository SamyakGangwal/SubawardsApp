from django.urls import path
from .views import *

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("", dashboard, name="dashboard"),
    path("subaward-request-tracking", create_subaward_request_tracking,
         name="create_subaward_request_tracking"),
    path('financial-compliance/<str:amendment_id>/', update_financial_compliance,
         name='update_financial_compliance'),
    path('list-records/', list_base_records, name='list_records'),
    path('subagreement-children/<str:amendment_id>/',
         list_subagreement_child_records, name='list_subagreement_child_records'),
    path('financial-comp-children/<str:amendment_id>/',
         list_financial_compliance_child_records, name='list_financial_compliance_child_records'),
#     path('create-subaward-amendment/<str:amendment_id>/', create_subaward_amendment, name='create_subaward_amendment'),
    path('update-subawards/<str:amendment_id>/', update_subaward_request_tracking, name='update_subaward_request_tracking'),
    path('view-subaward/<str:amendment_id>/', view_subaward_details, name='view_subaward_details'),
    path('view-financial-compliance/<str:amendment_id>/', view_financial_compliance, name='view_financial_compliance'),
]
