from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse

from games.models import Game
from reviews.forms import AddReviewForm, EditReviewForm, DeleteReviewForm
from reviews.models import Review
from django.views.generic import CreateView, UpdateView, DeleteView


class AddReviewView(CreateView):
    model = Review
    form_class = AddReviewForm
    template_name = 'reviews/review_form.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get_game(self):
        return get_object_or_404(Game, pk=self.kwargs['game_id'])

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.game = self.get_game()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = self.get_game().get_absolute_url()
        context['action'] = 'add'
        return context

    def get_success_url(self):
        return self.get_game().get_absolute_url()

class EditReviewView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = EditReviewForm
    template_name = 'reviews/review_form.html'

    def test_func(self):
        review = self.get_object()

        is_owner = self.request.user == review.user
        is_moderator = self.request.user.groups.filter(name='Moderators').exists()

        return is_owner or is_moderator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        context['cancel_url'] = self.object.game.get_absolute_url()
        return context

    def get_success_url(self):
        return reverse('game_details', kwargs={'game_id': self.object.game.pk})

class DeleteReviewView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_form.html'

    def test_func(self):
        review = self.get_object()

        is_owner = self.request.user == review.user
        is_moderator = self.request.user.groups.filter(name='Moderators').exists()

        return is_owner or is_moderator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DeleteReviewForm(instance=self.object)
        context['action'] = 'delete'
        context['cancel_url'] = self.object.game.get_absolute_url()
        return context

    def get_success_url(self):
        return reverse('game_details', kwargs={'game_id': self.object.game.pk})
