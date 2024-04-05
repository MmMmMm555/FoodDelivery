from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings 

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims such as user role, email
        token['role'] = user.role
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['access_token_lifetime'] = str(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])
        token['refresh_token_lifetime'] = str(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])

        return token