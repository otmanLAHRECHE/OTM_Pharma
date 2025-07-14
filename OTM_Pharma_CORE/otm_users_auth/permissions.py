from rest_framework import permissions


class IsRole(permissions.BasePermission):
    """
    Base permission class to restrict access based on the user's role.
    """
    role = None

    def has_permission(self, request, view):
        is_authenticated = request.user.is_authenticated
        if is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True
            is_role = getattr(request.user, "type_user", None) == self.type_user
            return is_role or request.user.type_user == "admin"
        return False

    def has_object_permission(self, request, view, obj):
        is_authenticated = request.user.is_authenticated
        if is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True
            is_role = getattr(request.user, "type_user", None) == self.type_user
            return is_role or request.user.type_user == "admin"
        return False
    



class IsPharmacist(IsRole):
    """
    Permission class allowing only Pharmacists or Admins.
    """
    role = "pharmacist"