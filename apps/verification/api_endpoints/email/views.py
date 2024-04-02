import datetime
import string

from django.conf import settings
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from . import serializers


EMAIL_CODE_TIMEOUT = 60 * 60  # 1 hour
EMAIL_RESEND_TIMEOUT = 60 * 2  # 2 minute
EMAIL_CODE_MAX_ATTEMPTS = 3  # 3 attempts
EMAIL_VERIFIED_EMAIl_TIMEOUT = 60 * 60 * 2  # 2 hour


class EmailSendCodeView(generics.GenericAPIView):
    """Sends code to email and returns uuid. And save uuid it need you to perform action"""
    serializer_class = serializers.EmailSendCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uuid = get_random_string(
            length=32, allowed_chars=string.ascii_letters + string.digits)
        code = get_random_string(length=6, allowed_chars=string.digits)
        old_sends = cache.get_many(cache.keys(
            f"{serializer.validated_data['email']}_*"))
        now = datetime.datetime.now()
        for old_send in old_sends:
            if (now - old_sends[old_send]['send_at']).total_seconds() < EMAIL_RESEND_TIMEOUT:
                raise ValidationError({
                    'email': 'email_code_already_sent'
                }, code='email_code_already_sent')

        data = {
            "email": serializer.validated_data['email'],
            "uuid": uuid,
            "code": code,
            "attempts": 0,
            "send_at": datetime.datetime.now(),
            'verified': False
        }
        cache.set(
            f"{serializer.validated_data['email']}_{uuid}",
            data,
            timeout=EMAIL_CODE_TIMEOUT
        )

        self.send_code(data)

        return Response(
            {'uuid': uuid},
            status=status.HTTP_200_OK
        )

    @staticmethod
    def send_code(data):
        subject = "'Food Delivery' verification"
        content = render_to_string('email/verification.html', context={'code':data['code']})
        msg = EmailMessage(
            subject, content, settings.EMAIL_HOST_USER, [data['email']])
        msg.content_subtype = "html"
        msg.send()


class EmailCheckCodeView(generics.GenericAPIView):
    """Checks code and returns verified status, get `uuid` from `email/SendCode`"""
    serializer_class = serializers.EmailCheckCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cache_data = cache.get_many(cache.keys(
            f"*_{serializer.validated_data['uuid']}"))
        data = None
        cache_key = None
        for key in cache_data:
            cache_key = key
            data = cache_data[key]
        if data is None or data['verified']:
            raise ValidationError({
                'code': 'email_invalid_code'
            }, code='email_invalid_code')

        if data['attempts'] > EMAIL_CODE_MAX_ATTEMPTS:
            raise ValidationError({
                'code': 'email_code_expired'
            }, code='email_code_expired')

        if data['code'] != serializer.validated_data['code']:
            data['attempts'] += 1
            cache.set(cache_key, data, timeout=EMAIL_CODE_TIMEOUT)
            raise ValidationError({
                'code': 'email_invalid_code'
            }, code='email_invalid_code')

        data['verified'] = True
        cache.set(cache_key, data, timeout=EMAIL_VERIFIED_EMAIl_TIMEOUT)

        return Response(
            {'verified': True},
            status=status.HTTP_200_OK
        )
