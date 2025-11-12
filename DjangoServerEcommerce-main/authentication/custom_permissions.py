from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Solo permite acceso a usuarios con rol ADMIN
    """
    def has_permission(self, request, view):  # type: ignore[override]
        return (
            request.user.is_authenticated and 
            request.user.roles.filter(id='ADMIN').exists()
        )


class IsAdminOrReadOnly(BasePermission):
    """
    Admin puede hacer todo, otros autenticados solo pueden leer (GET)
    """
    def has_permission(self, request, view):  # type: ignore[override]
        if not request.user.is_authenticated:
            return False
        
        # Métodos seguros (lectura)
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Métodos de escritura solo para ADMIN
        return request.user.roles.filter(id='ADMIN').exists()