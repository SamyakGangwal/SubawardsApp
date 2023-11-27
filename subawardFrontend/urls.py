from . import views
from django.urls import path

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("", views.dashboard, name="dashboard"),
    path("subaward-request-tracking", views.create_subaward_request_tracking,
         name="create_subaward_request_tracking"),
    path('financial-compliance/<str:amendment_id>/', views.update_financial_compliance,
         name='update_financial_compliance'),
    path('list-records/', views.list_base_records, name='list_records'),
    path('subagreement-children/<str:amendment_id>/',
         views.list_subagreement_child_records, name='list_subagreement_child_records'),
    path('financial-comp-children/<str:amendment_id>/',
         views.list_financial_compliance_child_records, name='list_financial_compliance_child_records'),
#     path('create-subaward-amendment/<str:amendment_id>/', create_subaward_amendment, name='create_subaward_amendment'),
    path('update-subawards/<str:amendment_id>/', views.update_subaward_request_tracking, name='update_subaward_request_tracking'),
    path('view-subaward/<str:amendment_id>/', views.view_subaward_details, name='view_subaward_details'),
    path('view-financial-compliance/<str:amendment_id>/', views.view_financial_compliance, name='view_financial_compliance'),
#     path('verify-email/', views.verify_email, name='verify-email'),
#     path('verify-email/done/', views.verify_email_done, name='verify-email-done'),
#     path('verify-email-confirm/<uidb64>/<token>/', views.verify_email_confirm, name='verify-email-confirm'),
#     path('verify-email/complete/', views.verify_email_complete, name='verify-email-complete'),
]
