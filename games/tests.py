from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from games.models import Game
from genres.models import Genre
from platforms.models import Platform
from games.forms import AddGameForm


# MODEL TESTS
# =========================

class GameModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass1234')
        self.genre = Genre.objects.create(name='Action', slug='action')
        self.platform = Platform.objects.create(name='PC', slug='pc')

    def test_game_creation(self):
        game = Game.objects.create(
            name='Test Game',
            description='This is a valid description',
            release_date='2020-01-01',
            created_by=self.user
        )

        game.genres.add(self.genre)
        game.platforms.add(self.platform)

        self.assertEqual(game.name, 'Test Game')

    def test_game_str(self):
        game = Game.objects.create(
            name='Game1',
            description='Valid description here',
            release_date='2020-01-01',
            created_by=self.user
        )
        self.assertEqual(str(game), 'Game1')

    def test_average_rating_none(self):
        game = Game.objects.create(
            name='Game2',
            description='Valid description here',
            release_date='2020-01-01',
            created_by=self.user
        )
        self.assertIsNone(game.average_rating())


# VIEW TESTS
# =========================

class GameViewsTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username='testuser', password='pass1234')

        self.genre = Genre.objects.create(name='Action', slug='action')
        self.platform = Platform.objects.create(name='PC', slug='pc')

        self.game = Game.objects.create(
            name='Game1',
            description='Valid description here',
            release_date='2020-01-01',
            created_by=self.user
        )

        self.game.genres.add(self.genre)
        self.game.platforms.add(self.platform)

    def test_games_list_view(self):
        response = self.client.get(reverse('games_list'))
        self.assertEqual(response.status_code, 200)

    def test_game_details_view(self):
        response = self.client.get(reverse('game_details', kwargs={'game_id': self.game.id}))
        self.assertEqual(response.status_code, 200)

    def test_add_game_requires_login(self):
        response = self.client.get(reverse('add_game'))
        self.assertNotEqual(response.status_code, 200)

    def test_add_game_logged_in(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.get(reverse('add_game'))
        self.assertEqual(response.status_code, 200)

    def test_games_by_genre(self):
        response = self.client.get(reverse('games_by_genre', kwargs={'slug': self.genre.slug}))
        self.assertEqual(response.status_code, 200)

    def test_games_by_platform(self):
        response = self.client.get(reverse('games_by_platform', kwargs={'slug': self.platform.slug}))
        self.assertEqual(response.status_code, 200)


# FORM TESTS
# =========================

class GameFormTests(TestCase):

    def setUp(self):
        self.genre = Genre.objects.create(name='Action', slug='action')
        self.platform = Platform.objects.create(name='PC', slug='pc')

    def test_valid_game_form(self):
        form = AddGameForm(data={
            'name': 'Game Form',
            'description': 'Valid description here',
            'release_date': '2020-01-01',
            'genres': [self.genre.id],
            'platforms': [self.platform.id],
        })

        self.assertTrue(form.is_valid())

    def test_invalid_short_name(self):
        form = AddGameForm(data={
            'name': 'A',
            'description': 'Valid description here',
            'release_date': '2020-01-01',
        })

        self.assertFalse(form.is_valid())

    def test_invalid_short_description(self):
        form = AddGameForm(data={
            'name': 'Valid Name',
            'description': 'short',
            'release_date': '2020-01-01',
        })

        self.assertFalse(form.is_valid())