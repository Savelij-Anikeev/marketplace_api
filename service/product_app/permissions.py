from rest_framework import permissions


class IsAdminOrVendorStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated and
            (request.user.is_staff or (request.user.role in ['vendor_staff', 'vendor_manager'] and
                                       request.user.work_place in obj.vendor.all())))

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and (request.user.role in ['vendor_staff', 'vendor_manager'] or
                                               request.user.is_staff)
        )

