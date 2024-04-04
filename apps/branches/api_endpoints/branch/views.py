from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.parsers import FormParser, MultiPartParser

from .serializers import BranchSerializer, BranchUpdateSerializer
from apps.branches.models import Branch
from apps.common.permissions import IsAdmin, IsWaiter


class BranchListCreateView(ListCreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAdmin | IsWaiter,]
    parser_classes = (FormParser, MultiPartParser)
    search_fields = ['name', 'address',]


class BranchRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchUpdateSerializer
    permission_classes = [IsAdmin | IsWaiter,]
    parser_classes = (FormParser, MultiPartParser)
    lookup_field = 'pk'
