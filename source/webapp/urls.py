from django.urls import path
from webapp.views.work_time_views import WorkTimeList, UserWorkTimeByMonth, WorkTimeStatsView
from webapp.views.branch_views import BranchCreateAPIView, BranchList, BranchDetail
from webapp.views.organization_views import OrganizationList, OrganizationDetail

urlpatterns = [
    path('branch/', BranchList.as_view(), name='branch_list'),
    path('branch/<int:pk>/', BranchDetail.as_view(), name='branch_detail'),
    path('branch/create/', BranchCreateAPIView.as_view(), name='create_branch'),
    path('organizations/', OrganizationList.as_view(), name='organization_list'),
    path('organizations/<int:pk>/', OrganizationDetail.as_view(), name='organization_detail'),
    path('work_time/', WorkTimeList.as_view(), name='work_time'),
    path('work_time_statistics/<int:user_id>/', WorkTimeStatsView.as_view()),
    path('<int:user_id>/work_time/<int:year>/<int:month>/', UserWorkTimeByMonth.as_view(),
         name='user_work_time_by_month'),
]