from rest_framework.serializers import ModelSerializer

from apps.branches.models import BranchComments, Branch
from apps.users.models import User


class CommentBranchSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = ('id', 'name',)


class CommentClientSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',)


class BranchCommentSerializer(ModelSerializer):
    class Meta:
        model = BranchComments
        fields = ('id', 'client', 'branch', 'rating', 'comment',)


class BranchCommentListSerializer(ModelSerializer):
    client = CommentClientSerializer(read_only=True)
    branch = CommentBranchSerializer(read_only=True)

    class Meta:
        model = BranchComments
        fields = ('id', 'branch', 'client', 'rating', 'comment', 'created_at', 'updated_at',)


class BranchCommentUpdateSerializer(ModelSerializer):
    class Meta:
        model = BranchComments
        fields = ('id', 'rating', 'comment',)
        extra_kwargs = {
            'rating': {'required': False},
        }