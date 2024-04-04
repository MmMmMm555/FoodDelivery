from rest_framework.serializers import ModelSerializer

from apps.foods.models import Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'image',)


class CategoryUpdateSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'image',)
        extra_kwargs = {
            'name': {'required': False},
            'image': {'required': False},
        }
