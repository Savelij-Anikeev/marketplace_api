from rest_framework.permissions import BasePermission


class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_staff or request.user.role == 'vendor_manager')
    
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_staff or request.user.role == 'vendor_manager')
