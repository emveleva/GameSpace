from datetime import date

from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.core.exceptions import ValidationError

from games.models import Game
from reviews.models import Review
from reviews.forms import AddReviewForm, DeleteReviewForm


# HELPERS
# =========================
def create_game(created_by, **kwargs):
    defaults = {
        "name": "Test Game",
        "release_date": date(2024, 1, 1),
        "created_by": created_by,  # ✅ FIX HERE
    }
    defaults.update(kwargs)
    return Game.objects.create(**defaults)


# MODEL TESTS
# =========================
class ReviewModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.game = create_game(created_by=self.user)  # ✅ FIX HERE

    def test_create_review_success(self):
        review = Review.objects.create(
            game=self.game,
            user=self.user,
            review='Great game!',
            rating=5
        )
        self.assertEqual(review.rating, 5)
        self.assertEqual(str(review), f"Review for {self.game.name} - Rating: 5")

    def test_rating_below_min_should_fail(self):
        review = Review(
            game=self.game,
            user=self.user,
            review='Bad',
            rating=0
        )
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_rating_above_max_should_fail(self):
        review = Review(
            game=self.game,
            user=self.user,
            review='Too good',
            rating=6
        )
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_review_blank_should_fail(self):
        review = Review(
            game=self.game,
            user=self.user,
            review='',
            rating=3
        )
        with self.assertRaises(ValidationError):
            review.full_clean()


# FORM TESTS
# =========================
class ReviewFormTests(TestCase):

    def test_valid_form(self):
        form = AddReviewForm(data={
            'rating': 4,
            'review': 'Nice game!'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_rating(self):
        form = AddReviewForm(data={
            'rating': 10,
            'review': 'Nice game!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_blank_review(self):
        form = AddReviewForm(data={
            'rating': 3,
            'review': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('review', form.errors)

    def test_delete_form_fields_disabled(self):
        form = DeleteReviewForm()
        for field in form.fields.values():
            self.assertTrue(field.disabled)


# VIEW TESTS
# =========================
class ReviewViewTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username='user', password='12345')
        self.other_user = User.objects.create_user(username='other', password='12345')

        self.moderator_group = Group.objects.create(name='Moderators')
        self.moderator = User.objects.create_user(username='mod', password='12345')
        self.moderator.groups.add(self.moderator_group)

        self.game = create_game(created_by=self.user)  # ✅ FIX HERE

        self.review = Review.objects.create(
            game=self.game,
            user=self.user,
            review='Good game',
            rating=4
        )

    def test_add_review_requires_login(self):
        url = reverse('add_review', kwargs={'game_id': self.game.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_add_review_post(self):
        self.client.login(username='user', password='12345')

        url = reverse('add_review', kwargs={'game_id': self.game.pk})
        response = self.client.post(url, {
            'rating': 5,
            'review': 'Amazing!'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 2)

    def test_edit_review_owner_access(self):
        self.client.login(username='user', password='12345')

        url = reverse('edit_review', kwargs={'pk': self.review.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_edit_review_other_user_denied(self):
        self.client.login(username='other', password='12345')

        url = reverse('edit_review', kwargs={'pk': self.review.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)

    def test_edit_review_moderator_allowed(self):
        self.client.login(username='mod', password='12345')

        url = reverse('edit_review', kwargs={'pk': self.review.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_delete_review_owner(self):
        self.client.login(username='user', password='12345')

        url = reverse('delete_review', kwargs={'pk': self.review.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 0)

    def test_delete_review_other_user_denied(self):
        self.client.login(username='other', password='12345')

        url = reverse('delete_review', kwargs={'pk': self.review.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 403)

    def test_delete_review_moderator_allowed(self):
        self.client.login(username='mod', password='12345')

        url = reverse('delete_review', kwargs={'pk': self.review.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)