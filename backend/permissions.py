from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        print('- ПЕРМИШИН - МЫ ТУТ      has_object_permission')
        if request.method == 'GET':
            return True
        return request.user == obj.user

