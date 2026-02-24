from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy

from games.models import Game
from reviews.forms import AddReviewForm, EditReviewForm, DeleteReviewForm
from reviews.models import Review
from django.views.generic import CreateView, UpdateView, DeleteView


class AddReviewView(CreateView):
    model = Review
    form_class = AddReviewForm
    template_name = 'reviews/review_form.html'

    def get_game(self):
        return get_object_or_404(Game, pk=self.kwargs['game_id'])

    def form_valid(self, form):
        form.instance.game = self.get_game()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = self.get_game().get_absolute_url()
        context['action'] = 'add'
        return context

    def get_success_url(self):
        return self.get_game().get_absolute_url()

class EditReviewView(UpdateView):
    model = Review
    form_class = EditReviewForm
    template_name = 'reviews/review_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        context['cancel_url'] = self.object.game.get_absolute_url()
        return context

    def get_success_url(self):
        return reverse('game_details', kwargs={'game_id': self.object.game.pk})

class DeleteReviewView(DeleteView):
    model = Review
    template_name = 'reviews/review_form.html'
    success_url = reverse_lazy('games_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = self.object

        context['form'] = DeleteReviewForm(instance=obj)
        context['action'] = 'delete'
        context['cancel_url'] = obj.game.get_absolute_url()

        return context
