from rest_framework import serializers
from apps.users.models import User
from apps.verification.utils import email_check_verified
from rest_framework_simplejwt.tokens import RefreshToken


class RegistrationWithEmailSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField()
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password", "uuid")

    def validate(self, data):
        uuid = data.pop("uuid")
        email = data["email"]
        if email_check_verified(uuid, email) is not True:
            raise serializers.ValidationError(
                "Email is not verified", code="not_verified_email_uuid")
        return data

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Email already exists", code="already_exists")
        return email

    def save(self, **kwargs):
        user = User(
            email=self.validated_data["email"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
        )
        user.set_password(self.validated_data["password"])
        user.save()
        self.instance = user
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
