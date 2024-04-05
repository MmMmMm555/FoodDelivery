from rest_framework.serializers import ModelSerializer, ListField, ImageField

from apps.foods.api_endpoints.category.serializers import CategorySerializer
from apps.foods.models import Food, FoodImages


class FoodImagesListSerializer(ModelSerializer):
    class Meta:
        model = FoodImages
        fields = ('image',)


class FoodCreateSerializer(ModelSerializer):
    images_list = ListField(child=ImageField(), required=False,)

    class Meta:
        model = Food
        fields = ('id', 'name', 'price', 'category',
                  'images_list', 'available',)

    def create(self, validated_data):
        images = validated_data.pop('images_list', [])
        food = Food.objects.create(**validated_data)
        for image in images:
            FoodImages.objects.create(food=food, image=image)
        return food


class FoodUpdateSerializer(ModelSerializer):
    class Meta:
        model = Food
        fields = ('id', 'name', 'price', 'category', 'available',)
        extra_kwargs = {
            'name': {'required': False},
            'price': {'required': False},
            'images': {'required': False},
            'category': {'required': False},
        }


class FoodListSerializer(ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    images = FoodImagesListSerializer(many=True, read_only=True)

    class Meta:
        model = Food
        fields = ('id', 'name', 'price', 'images', 'category', 'available',)
        read_only_fields = fields
