from django.urls import path
from webapp.views.branch_views import BranchDetail, BranchList
from webapp.views.organization_views import OrganizationList, OrganizationDetail

urlpatterns = [
    path('branch/', BranchList.as_view(), name='branch_list'),
    path('branch/<int:pk>/', BranchDetail.as_view(), name='branch_detail'),
    path('organizations/', OrganizationList.as_view(), name='organization_list'),
    path('organizations/<int:pk>/', OrganizationDetail.as_view(), name='organization_detail'),
]