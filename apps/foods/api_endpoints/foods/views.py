from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import AllowAny

from .serializers import (FoodCreateSerializer,
                          FoodListSerializer, FoodUpdateSerializer)
from apps.foods.models import Food
from apps.common.permissions import IsAdmin, IsWaiter


class FoodListCreateView(ListCreateAPIView):
    queryset = Food.objects.all().select_related(
        'category').prefetch_related('images')
    serializer_class = FoodCreateSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAdmin | IsWaiter,)
    search_fields = ('name',)
    filterset_fields = ('category', 'available',)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return FoodListSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.request.method == 'GET':
            return (AllowAny(),)
        return super().get_permissions()


class FoodRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all().select_related(
        'category').prefetch_related('images')
    serializer_class = FoodUpdateSerializer
    parser_classes = (MultiPartParser, JSONParser)
    permission_classes = (IsAdmin | IsWaiter,)
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.method == "GET":
            return FoodListSerializer
        return self.serializer_class
