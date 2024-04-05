from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.parsers import FormParser, MultiPartParser

from .serializers import BranchCommentListSerializer, BranchCommentSerializer, BranchCommentUpdateSerializer
from apps.branches.models import BranchComments
from apps.common.permissions import IsClient, IsAdmin, IsCommentOwner


class CommentListCreateView(ListCreateAPIView):
    queryset = BranchComments.objects.all().select_related('branch', 'client')
    serializer_class = BranchCommentSerializer
    parser_classes = (FormParser,)
    permission_classes = (IsClient,)
    filterset_fields = ('branch', 'rating')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BranchCommentListSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class CommentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = BranchComments.objects.all().select_related('branch', 'client')
    serializer_class = BranchCommentUpdateSerializer
    parser_classes = (FormParser, MultiPartParser,)
    permission_classes = (IsCommentOwner or IsAdmin,)
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BranchCommentListSerializer
        return super().get_serializer_class()
