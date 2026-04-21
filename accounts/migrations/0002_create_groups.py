from django.db import migrations


def get_perm(apps, app_label, codename):
    Permission = apps.get_model('auth', 'Permission')
    return Permission.objects.filter(
        content_type__app_label=app_label,
        codename=codename
    ).first()


def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')

    # Game Permissions
    # -------------------------
    game_perms = [
        get_perm(apps, 'games', 'add_game'),
        get_perm(apps, 'games', 'change_game'),
        get_perm(apps, 'games', 'delete_game'),
    ]

    # Review Permissions
    # -------------------------
    review_perms = [
        get_perm(apps, 'reviews', 'add_review'),
        get_perm(apps, 'reviews', 'change_review'),
        get_perm(apps, 'reviews', 'delete_review'),
    ]

    # Platform Permissions
    # -------------------------
    platform_perms = [
        get_perm(apps, 'platforms', 'add_platform'),
        get_perm(apps, 'platforms', 'change_platform'),
        get_perm(apps, 'platforms', 'delete_platform'),
    ]

    # Genre Permissions
    # -------------------------
    genre_perms = [
        get_perm(apps, 'genres', 'add_genre'),
        get_perm(apps, 'genres', 'change_genre'),
        get_perm(apps, 'genres', 'delete_genre'),
    ]

    # Users Group Permissions
    # -------------------------
    users_group_permissions = [
        p for p in (
            game_perms +
            review_perms +
            platform_perms +
            genre_perms
        ) if p is not None
    ]

    # Moderators Group Permissions
    # -------------------------
    moderators_group_permissions = [
        p for p in [
            get_perm(apps, 'reviews', 'change_review'),
            get_perm(apps, 'reviews', 'delete_review'),
        ] if p is not None
    ]

    # Groups
    # -------------------------
    users_group, _ = Group.objects.get_or_create(name='Users')
    moderators_group, _ = Group.objects.get_or_create(name='Moderators')

    # Assign permissions
    # -------------------------
    users_group.permissions.set(users_group_permissions)
    moderators_group.permissions.set(moderators_group_permissions)


def remove_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['Users', 'Moderators']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('games', '0001_initial'),
        ('reviews', '0001_initial'),
        ('platforms', '0001_initial'),
        ('genres', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups, remove_groups),
    ]