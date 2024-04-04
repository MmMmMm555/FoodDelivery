from rest_framework.serializers import ModelSerializer
from django.contrib.gis.geos import Point

from apps.branches.models import Branch


class BranchSerializer(ModelSerializer):

    class Meta:
        model = Branch
        fields = ('id', 'name', 'address', 'branch_contact',
                  'branch_foods', 'longitude', 'latitude',)

    def create(self, validated_data):
        branch = super().create(validated_data)
        location = Point(validated_data.get('latitude'),
                         validated_data.get('longitude'), srid=4326)
        branch.location = location
        branch.save()
        return branch


class BranchUpdateSerializer(ModelSerializer):

    class Meta:
        model = Branch
        fields = ('id', 'name', 'address', 'branch_contact',
                  'branch_foods',)
        extra_kwargs = {
            'name': {'required': False},
            'address': {'required': False},
            'branch_contact': {'required': False},
            'branch_foods': {'required': False},
        }
