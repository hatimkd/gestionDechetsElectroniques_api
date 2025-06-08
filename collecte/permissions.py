from rest_framework import permissions

class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Client').exists()
class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        print("User:", request.user)
        print("Authenticated:", request.user.is_authenticated)

    
        print("Groups:", request.user.groups.all())
        return request.user and request.user.is_authenticated and request.user.groups.filter(name="Manager").exists()
            
        
        
        
        # return True  # TEMPORAIRE : autoriser tout le monde


class IsLogisticien(permissions.BasePermission):
    def has_permission(self, request, view):
        
        print("User:", request.user)
        print("Authenticated:", request.user.is_authenticated)

    
        print("Groups:", request.user.groups.all())
        return request.user.is_authenticated and request.user.groups.filter(name="Logisticien").exists()

class IsTechnicien(permissions.BasePermission):
    def has_permission(self, request, view):
        
        # return request.user.groups.filter(name='Technicien').exists()
        
        return request.user.is_authenticated and request.user.groups.filter(name="Technicien").exists()
        

class IsTechnicienManager(permissions.BasePermission):
    def has_permission(self, request, view):
        
        # return request.user.groups.filter(name='Technicien').exists()
        
        return request.user.is_authenticated and request.user.groups.filter(name="Technicien").exists()     or    request.user.groups.filter(name="Manager").exists()
class IsLogisticienOrManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.groups.filter(name="Logisticien").exists()
                or request.user.groups.filter(name="Manager").exists()
            )
        )