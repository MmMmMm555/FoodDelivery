from django.core.validators import RegexValidator
from rest_framework import serializers


class EmailSendCodeSerializer(serializers.Serializer):  # noqa
    email = serializers.EmailField(max_length=254, required=True)


class EmailCheckCodeSerializer(serializers.Serializer):  # noqa
    uuid = serializers.CharField(max_length=64, required=True)
    code = serializers.CharField(max_length=6, required=True)
