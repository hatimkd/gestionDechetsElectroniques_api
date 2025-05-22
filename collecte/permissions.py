from rest_framework import permissions

class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Client').exists()

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists()

class IsLogisticien(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Logisticien').exists()

class IsTechnicien(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Technicien').exists()
