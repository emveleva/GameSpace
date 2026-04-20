from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta

from accounts.models import Profile
from accounts.forms import RegisterForm
from games.models import Game
from reviews.models import Review


# MODEL TESTS
# =========================

class ProfileModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass1234')
        self.profile = self.user.profile

    def test_profile_str(self):
        self.assertEqual(str(self.profile), 'testuser')

    def test_valid_birthday(self):
        self.profile.birthday = date(2000, 1, 1)
        self.profile.full_clean()

    def test_future_birthday_raises_error(self):
        self.profile.birthday = date.today() + timedelta(days=1)
        with self.assertRaises(Exception):
            self.profile.full_clean()

    def test_name_min_length(self):
        self.profile.name = 'A'
        with self.assertRaises(Exception):
            self.profile.full_clean()

    def test_city_min_length(self):
        self.profile.city = 'B'
        with self.assertRaises(Exception):
            self.profile.full_clean()

    def test_favorite_games(self):
        game = Game.objects.create(
            name='Game1',
            description='Valid description here',
            release_date=date(2020, 1, 1),
            created_by=self.user
        )
        self.profile.favorite_games.add(game)
        self.assertIn(game, self.profile.favorite_games.all())

    def test_reviews_property(self):
        self.assertEqual(self.profile.reviews.count(), 0)


# VIEW TESTS
# =========================

class AccountViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass1234')

    def test_register_view_loads(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertNotEqual(response.status_code, 200)

    def test_dashboard_logged_in(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_logout_redirect(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_profile_details_view(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.get(reverse('profile-details'))
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_view(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)

    def test_delete_profile_view(self):
        self.client.login(username='testuser', password='pass1234')

        response = self.client.post(reverse('delete_profile'), follow=True)

        self.assertEqual(response.status_code, 200)

    def test_dashboard_context(self):
        self.client.login(username='testuser', password='pass1234')

        game = Game.objects.create(
            name="Game1",
            description='Valid description here',
            release_date=date(2020, 1, 1),
            created_by=self.user
        )

        Review.objects.create(
            game=game,
            user=self.user,
            rating=5
        )

        response = self.client.get(reverse('dashboard'))

        self.assertIn('games_count', response.context)
        self.assertIn('reviews_count', response.context)


# FORM TESTS
# =========================

class RegisterFormTests(TestCase):

    def test_valid_form(self):
        form = RegisterForm(data={
            'username': 'user1',
            'email': 'test@test.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertTrue(form.is_valid())

    def test_duplicate_email(self):
        User.objects.create_user(
            username='user1',
            email='test@test.com',
            password='pass1234'
        )

        form = RegisterForm(data={
            'username': 'user2',
            'email': 'test@test.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })

        self.assertFalse(form.is_valid())