from django.urls import path
from .api_endpoints.email import views as email_views

app_name = "verification_service"

urlpatterns = [
    path('send-code', view=email_views.EmailSendCodeView.as_view(), name='EmailSendCode'),
    path('check-code', view=email_views.EmailCheckCodeView.as_view(), name='EmailCheckCode'),
]
