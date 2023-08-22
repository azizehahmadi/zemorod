from rest_framework import permissions
from .models import Profile, User


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.profile.role == 'ADMIN'

class IsSellerUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.profile.role == 'SELLER'


class IsBuyerUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.profile.role == 'BUYER'

class CanEditAndRegisterProfile(permissions.BasePermission):
    class CanEditProfile(permissions.BasePermission):

        def has_object_permission(self, request, view, obj):
            if request.user.profile.role == 'ADMIN':
                return True
            elif obj.user == request.user:
                return True
            return False



