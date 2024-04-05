from rest_framework.permissions import BasePermission
from apps.users.models import UserRoles


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == UserRoles.ADMIN


class IsWaiter(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == UserRoles.WAITER


class IsClient(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == UserRoles.CLIENT


class IsCommentOwner(BasePermission):
    def has_permission(self, request, view):
        return view.get_object().client == request.user
