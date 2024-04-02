from django.urls import path

from apps.verification.api_endpoints.email import views as email_views
from apps.users.api_endpoints.register.views import RegistrationWithEmailView
from apps.users.api_endpoints.login.views import LoginObtainTokenPairView
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView)
from apps.users.api_endpoints.create_waiter.views import (
    WaiterCreateView, WaiterUpdateRetrieveDestroyView)

app_name = 'verification'

urlpatterns = [
    # email verification
    path('send-code', view=email_views.EmailSendCodeView.as_view(),
         name='EmailSendCode'),
    path('check-code', view=email_views.EmailCheckCodeView.as_view(),
         name='EmailCheckCode'),

    # register login
    path('register/', RegistrationWithEmailView.as_view(),
         name='user_registration'),
    path('login/', LoginObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('refresh_token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify_token/', TokenVerifyView.as_view(), name='token_verify'),

    # waiter
    path('waiter/', WaiterCreateView.as_view(), name='waiter_create_list'),
    path('waiter/<int:pk>', WaiterUpdateRetrieveDestroyView.as_view(),
         name='waiter_retrieve_update_delete'),
]
