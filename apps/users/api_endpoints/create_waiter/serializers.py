from rest_framework.serializers import ModelSerializer

from apps.users.models import User, UserRoles
from apps.branches.models import Branch


class BranchSerializerForWaiter(ModelSerializer):
    class Meta:
        model = Branch
        fields = ('id', 'name', 'address',)


class WaiterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'email', 'branch', 'password',)
        extra_kwargs = {
            'branch': {'required': True},
            'first_name': {'required': True},
        }

    def create(self, validated_data):
        waiter = User.objects.create_user(**validated_data)
        waiter.role = UserRoles.WAITER
        waiter.save()
        return waiter


class WaiterUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'branch', 'password',)
        extra_kwargs = {'password': {'required': False}}


class WaiterListSerializer(ModelSerializer):
    branch = BranchSerializerForWaiter(many=False)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'email', 'branch',)