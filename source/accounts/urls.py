from django.urls import path
from accounts.views import UserList, UserDetail

aa_name = "accounts"

urlpatterns = [
    path('user/', UserList.as_view(), name='user_list'),
    path('user/<int:pk>/', UserDetail.as_view(), name='user_detail'),
]