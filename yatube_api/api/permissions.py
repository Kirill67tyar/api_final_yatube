from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrAuthenticatedReadOnly(BasePermission):

    def has_permission(self, request, view):
        """Доступ разрушён в если клиент аутентифицирован."""
        return request.user.is_authenticated or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        """
        Доступ разрушён в 1м из 2х случаев:
        1 - клиент автор поста.
        2 - HTTP метод - GET | HEAD | OPTIONS.
        Т.е. если не админ и не автор поста, то изменять и удалять нельзя.
        """
        return request.user == obj.author or request.method in SAFE_METHODS
