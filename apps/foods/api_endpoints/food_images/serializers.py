from rest_framework.serializers import ModelSerializer

from apps.foods.models import FoodImages


class FoodImagesSerializer(ModelSerializer):
    class Meta:
        model = FoodImages
        fields = ('id', 'food', 'image',)