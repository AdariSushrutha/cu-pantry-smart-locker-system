from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    """Only students can access"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.groups.filter(name='Student').exists()
        )


class IsVolunteer(BasePermission):
    """Volunteers, Managers and Admins can access"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.groups.filter(
                name__in=['Volunteer', 'Manager', 'Admin']
            ).exists() or request.user.is_superuser
        )


class IsManager(BasePermission):
    """Managers and Admins can access"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.groups.filter(
                name__in=['Manager', 'Admin']
            ).exists() or request.user.is_superuser
        )


class IsAdmin(BasePermission):
    """Only Admins can access"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.groups.filter(name='Admin').exists()
            or request.user.is_superuser
        )


class IsStudentOrVolunteer(BasePermission):
    """Students, Volunteers, Managers and Admins can access"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.groups.filter(
                name__in=['Student', 'Volunteer', 'Manager', 'Admin']
            ).exists() or request.user.is_superuser
        )