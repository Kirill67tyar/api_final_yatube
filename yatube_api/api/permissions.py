from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly


class IsAuthorOrAuthenticatedReadOnly(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        """
        Доступ разрешён в 1м из 2х случаев:
        1 - клиент автор поста.
        2 - HTTP метод - GET | HEAD | OPTIONS.
        Т.е. если не автор поста, то изменять и удалять нельзя.
        """
        return request.user == obj.author or request.method in SAFE_METHODS
