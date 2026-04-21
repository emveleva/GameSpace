from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsCreatorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.created_by == request.user

def is_moderator(user):
    return user.groups.filter(name='Moderators').exists()


def can_modify_game(user, game):
    if user.is_superuser:
        return True

    if is_moderator(user):
        return True

    return game.created_by == user