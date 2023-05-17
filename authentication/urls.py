from django.urls import path
from .views import RegisterView, VerifyEmail, LoginView, PasswordResetEmailView, PasswordTokenCheckView, PasswordResetEmailView, SetNewPasswordView 
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', RegisterView.as_view(), name = 'register'),
    path('email-verify/', VerifyEmail.as_view(), name = 'email-verify'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset-email', PasswordResetEmailView.as_view(), name='password-reset-email'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordTokenCheckView.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordView.as_view(), name='password-reset-completes')
    
]