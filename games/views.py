from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Avg, Q
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DeleteView, UpdateView, CreateView, DetailView

from accounts.models import Profile
from common.mixins import DisableFieldsMixin
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

        if self.request.user.is_authenticated:
            context['is_favorite'] = self.request.user.profile.favorite_games.filter(
                id=self.object.id
            ).exists()
        else:
            context['is_favorite'] = False

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


class AddGameView(LoginRequiredMixin, CreateView):
    model = Game
    form_class = AddGameForm
    template_name = 'games/game_form.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'add'
        context['cancel_url'] = reverse_lazy('games_list')
        context['genres_count'] = Genre.objects.count()
        context['platforms_count'] = Platform.objects.count()
        return context

    def get_success_url(self):
        return reverse_lazy('game_details', kwargs={'game_id': self.object.id})


class EditGameView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Game
    form_class = EditGameForm
    template_name = 'games/game_form.html'
    pk_url_kwarg = 'game_id'

    def test_func(self):
        return self.get_object().created_by == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        context['cancel_url'] = self.object.get_absolute_url()
        context['genres_count'] = Genre.objects.count()
        context['platforms_count'] = Platform.objects.count()
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

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['action'] = 'delete'
        context['cancel_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)

class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, game_id):
        game = get_object_or_404(Game, id=game_id)

        profile = Profile.objects.get(user=request.user)

        if game in profile.favorite_games.all():
            profile.favorite_games.remove(game)
            favorited = False
        else:
            profile.favorite_games.add(game)
            favorited = True

        return JsonResponse({
            "favorited": favorited
        })