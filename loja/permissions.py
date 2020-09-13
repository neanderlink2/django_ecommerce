from rest_framework.permissions import BasePermission

class CreanteAndReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        return request.method in ['GET', 'POST']

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        elif request.method in ['GET']:
            return True
        return False
