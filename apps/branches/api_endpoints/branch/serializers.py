from rest_framework.serializers import ModelSerializer

from apps.branches.models import Branch


class BranchSerializer(ModelSerializer):

    class Meta:
        model = Branch
        fields = ('id', 'name', 'address', 'branch_contact',
                  'branch_foods', 'location',)


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
