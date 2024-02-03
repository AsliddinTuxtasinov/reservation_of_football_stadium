from rest_framework import permissions

from accounts.enums import AccountRoleEnums


class SuperAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.user_roles == AccountRoleEnums.ADMIN
        )


class StadiumOwnerAndAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.user_roles in [AccountRoleEnums.ADMIN, AccountRoleEnums.STADIUM_OWNER]
        )

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to access the object.
        """
        if request.user.user_roles == AccountRoleEnums.ADMIN:
            return True
        elif request.user.user_roles == AccountRoleEnums.STADIUM_OWNER:
            return obj.owner == request.user if obj.owner else False
        return False


class UserAndAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.user_roles in [AccountRoleEnums.ADMIN, AccountRoleEnums.USER]
        )
