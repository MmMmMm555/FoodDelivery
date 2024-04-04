from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from .serializers import FoodImagesSerializer
from apps.foods.models import FoodImages
from apps.common.permissions import IsAdmin, IsWaiter


class FoodImagesListCreateView(ListCreateAPIView):
    queryset = FoodImages.objects.all()
    serializer_class = FoodImagesSerializer
    parser_classes = (FormParser,)
    permission_classes = (IsAdmin | IsWaiter,)


class FoodImagesRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = FoodImages.objects.all()
    serializer_class = FoodImagesSerializer
    permission_classes = (IsAdmin | IsWaiter,)
    parser_classes = (FormParser,)
    lookup_field = 'pk'
