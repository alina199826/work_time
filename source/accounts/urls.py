from django.urls import path
from accounts.views import UserList, UserDetail
from accounts.views import UserRegistrationView, VerifyEmailView


aa_name = "accounts"

urlpatterns = [
    path('user/', UserList.as_view(), name='user_list'),
    path('user/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
]

