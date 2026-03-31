
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Q
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DeleteView, UpdateView, CreateView, DetailView

from games.forms import AddGameForm, EditGameForm, DeleteGameForm, GameSearchForm
from games.models import Game, Genre, Platform

class GamesListView(TemplateView):
    template_name = 'games/games_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_form = GameSearchForm(self.request.GET or None)

        games = Game.objects.annotate(
            avg_rating=Avg('reviews__rating')
        ).order_by('name')

        if 'query' in self.request.GET and search_form.is_valid():
            search_value = search_form.cleaned_data['query']
            games = games.filter(
                Q(name__icontains=search_value) |
                Q(description__icontains=search_value)
            )

        context['games'] = games
        context['page_title'] = 'All Games'
        context['search_form'] = search_form

        return context


class GameDetailsView(DetailView):
    model = Game
    template_name = 'games/game_details.html'
    pk_url_kwarg = 'game_id'
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['avg_rating'] = self.object.reviews.aggregate(
            Avg('rating')
        )['rating__avg']
        return context


class GamesByGenreView(TemplateView):
    template_name = 'games/games_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        genre = get_object_or_404(Genre, slug=self.kwargs['slug'])
        search_form = GameSearchForm(self.request.GET or None)

        games = Game.objects.filter(genres=genre)

        if 'query' in self.request.GET and search_form.is_valid():
            search_value = search_form.cleaned_data['query']
            games = games.filter(
                Q(name__icontains=search_value) |
                Q(description__icontains=search_value)
            )

        context['games'] = games
        context['page_title'] = f'Games in {genre.name}'
        context['search_form'] = search_form
        context['current_genre'] = genre
        context['show_genre_actions'] = True
        context['current_platform'] = None
        context['show_platform_actions'] = False

        return context


class GamesByPlatformView(TemplateView):
    template_name = 'games/games_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        platform = get_object_or_404(Platform, slug=self.kwargs['slug'])
        search_form = GameSearchForm(self.request.GET or None)

        games = Game.objects.filter(platforms=platform)

        if 'query' in self.request.GET and search_form.is_valid():
            search_value = search_form.cleaned_data['query']
            games = games.filter(
                Q(name__icontains=search_value) |
                Q(description__icontains=search_value)
            )

        context['games'] = games
        context['page_title'] = f'Games on {platform.name}'
        context['search_form'] = search_form
        context['current_platform'] = platform
        context['show_platform_actions'] = True
        context['current_genre'] = None
        context['show_genre_actions'] = False

        return context


class AddGameView(CreateView):
    model = Game
    form_class = AddGameForm
    template_name = 'games/game_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'add'
        context['cancel_url'] = reverse_lazy('games_list')
        context['genres_count'] = Genre.objects.count()
        context['platforms_count'] = Platform.objects.count()
        return context

    def get_success_url(self):
        return reverse_lazy('game_details', kwargs={'game_id': self.object.id})


class EditGameView(UpdateView):
    model = Game
    form_class = EditGameForm
    template_name = 'games/game_form.html'
    pk_url_kwarg = 'game_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        context['cancel_url'] = self.object.get_absolute_url()
        return context

    def get_success_url(self):
        return reverse_lazy('game_details', kwargs={'game_id': self.object.id})


class DeleteGameView(DeleteView):
    model = Game
    template_name = 'games/game_form.html'
    success_url = reverse_lazy('games_list')
    pk_url_kwarg = 'game_id'

    def get_form(self, form_class=None):
        form = DeleteGameForm(instance=self.object)

        for field in form.fields.values():
            field.disabled = True

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['action'] = 'delete'
        context['cancel_url'] = self.object.get_absolute_url()
        return context