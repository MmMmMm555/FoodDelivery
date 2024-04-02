from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.parsers import FormParser

from .serializers import (WaiterSerializer, WaiterUpdateSerializer, WaiterListSerializer)
from apps.users.models import User, UserRoles
from apps.common.permissions import IsAdmin



class WaiterCreateView(ListCreateAPIView):
    """
    Create a new waiter.
    """
    queryset = User.objects.filter(role=UserRoles.WAITER).select_related('branch')
    serializer_class = WaiterSerializer
    permission_classes = [IsAdmin]
    parser_classes = (FormParser,)
    filterset_fields = ['branch']
    search_fields = ['email', 'first_name', 'last_name']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WaiterListSerializer
        return self.serializer_class


class WaiterUpdateRetrieveDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(role=UserRoles.WAITER).select_related('branch')
    serializer_class = WaiterUpdateSerializer
    permission_classes = [IsAdmin]
    parser_classes = (FormParser,)
    lookup_field = 'pk'
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WaiterListSerializer
        return self.serializer_class
