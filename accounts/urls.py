from django.urls import path
from .views import (
    RegisterUserView,
    VerifyUserEmailView,
    LoginUserView,
    TestAuthenticateRequest
)
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [

    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify-email/', VerifyUserEmailView.as_view(), name='verify'),
    path('tokens/refersh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('profile/', TestAuthenticateRequest.as_view(), name='profile')

]