from rest_framework import generics
from . import serializers
from apps.users.models import User


class RegistrationWithEmailView(generics.CreateAPIView):
    serializer_class = serializers.RegistrationWithEmailSerializer
    queryset = User.objects.all()
