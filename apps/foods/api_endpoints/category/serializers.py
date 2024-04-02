from rest_framework.serializers import ModelSerializer

from apps.foods.models import Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)


class CategoryUpdateSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)
        extra_kwargs = {
            'name': {'required': False},
        }
