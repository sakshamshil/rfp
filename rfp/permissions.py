from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    message = "Authorization failed"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "admin"
    


class IsVendor(permissions.BasePermission):
    message = "Authorization failed"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "vendor"