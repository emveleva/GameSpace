from django.db import migrations

def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Game Permissions
    # -------------------------
    game_perms = Permission.objects.filter(content_type__app_label='games')
    add_game = game_perms.get(codename='add_game')
    change_game = game_perms.get(codename='change_game')
    delete_game = game_perms.get(codename='delete_game')

    # Review Permissions
    # -------------------------
    review_perms = Permission.objects.filter(content_type__app_label='reviews')
    add_review = review_perms.get(codename='add_review')
    change_review = review_perms.get(codename='change_review')
    delete_review = review_perms.get(codename='delete_review')


    # Platform Permissions
    # -------------------------
    platform_perms = Permission.objects.filter(content_type__app_label='platforms')
    add_platform = platform_perms.get(codename='add_platform')
    change_platform = platform_perms.get(codename='change_platform')
    delete_platform = platform_perms.get(codename='delete_platform')

    # -------------------------
    # Genre Permissions
    # -------------------------
    genre_perms = Permission.objects.filter(content_type__app_label='genres')
    add_genre = genre_perms.get(codename='add_genre')
    change_genre = genre_perms.get(codename='change_genre')
    delete_genre = genre_perms.get(codename='delete_genre')

    # Groups
    # -------------------------
    users_group, _ = Group.objects.get_or_create(name='Users')
    moderators_group, _ = Group.objects.get_or_create(name='Moderators')

    # Users Group Permissions
    # -------------------------
    users_group.permissions.set([
        add_game, change_game, delete_game,
        add_review, change_review, delete_review,
        add_platform, change_platform, delete_platform,
        add_genre, change_genre, delete_genre,
    ])

    # Moderators Group Permissions
    # -------------------------
    moderators_group.permissions.set([
        change_review, delete_review,
    ])


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