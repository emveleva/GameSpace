def is_moderator(user):
    return user.groups.filter(name='Moderators').exists()


def can_modify_review(user, review):
    if user.is_superuser:
        return True

    if is_moderator(user):
        return True

    return review.user == user