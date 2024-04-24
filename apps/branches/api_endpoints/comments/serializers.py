from rest_framework.serializers import ModelSerializer, ValidationError

from apps.branches.models import BranchComments, Branch
from apps.users.models import User
from django.contrib.gis.geos import GEOSGeometry

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
        fields = ('id', 'client', 'branch', 'rating', 'comment', 'area',)

    def validate(self, attrs):
        point = GEOSGeometry(attrs['branch'].location)
        polygon = GEOSGeometry(attrs['area'])
        if not point.within(polygon):
            raise ValidationError('you can not comment here')
        return super().validate(attrs)
    

class BranchCommentListSerializer(ModelSerializer):
    client = CommentClientSerializer(read_only=True)
    branch = CommentBranchSerializer(read_only=True)

    class Meta:
        model = BranchComments
        fields = ('id', 'branch', 'client', 'rating', 'comment', 'area', 'created_at', 'updated_at',)


class BranchCommentUpdateSerializer(ModelSerializer):
    class Meta:
        model = BranchComments
        fields = ('id', 'rating', 'comment',)
        extra_kwargs = {
            'rating': {'required': False},
        }