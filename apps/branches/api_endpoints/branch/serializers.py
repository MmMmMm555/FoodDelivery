from rest_framework.serializers import ModelSerializer

from apps.branches.models import Branch


class BranchSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = ('id', 'name', 'address', 'longitude', 'latitude',)


class BranchUpdateSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = ('id', 'name', 'address', 'longitude', 'latitude',)
        extra_kwargs = {
            'name': {'required': False},
            'address': {'required': False},
            'longitude': {'required': False},
            'latitude': {'required': False},
        }
