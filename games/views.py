from collections import defaultdict

from django.contrib.admin.templatetags.admin_list import search_form
from django.db.models.functions import Lower
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Q
from django.urls import reverse

from games.forms import AddGameForm, EditGameForm, DeleteGameForm, GameSearchForm
from games.models import Game, Genre, Platform


def games_list(request: HttpRequest):
    search_form = GameSearchForm(request.GET or None)

    list_games = Game.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('name')

    if 'query' in request.GET:
        if search_form.is_valid():
            search_value = search_form.cleaned_data['query']
            list_games = list_games.filter(
                Q(name__icontains=search_value)
                    |
                Q(description__icontains=search_value)
            )

    context = {
        'games': list_games,
        'page_title': 'All Games',
        'search_form': search_form,
    }

    return render(request, 'games/games_list.html', context)

def game_details(request: HttpRequest, game_id: str):
    game = get_object_or_404(Game, id=game_id)

    avg_rating = game.reviews.aggregate(Avg('rating'))['rating__avg']

    context = {
        'game': game,
        'avg_rating': avg_rating,
    }
    return render(request, 'games/game_details.html', context)

def genres_list(request: HttpRequest):
    genres = Genre.objects.annotate(
        lower_name=Lower('name')
    ).order_by('lower_name')

    grouped_genres = defaultdict(list)

    for genre in genres:
        first_letter = genre.name[0].upper()
        grouped_genres[first_letter].append(genre)

    context = {
        'grouped_genres': dict(sorted(grouped_genres.items())),
        'page_title': 'All Genres',
    }

    return render(request, 'games/genres_list.html', context)

def games_by_genre(request: HttpRequest, slug: str):
    genre = get_object_or_404(Genre, slug=slug)
    search_form = GameSearchForm(request.GET or None)

    games = Game.objects.filter(genres=genre)

    if 'query' in request.GET:
        if search_form.is_valid():
            search_value = search_form.cleaned_data['query']
            games = games.filter(
                Q(name__icontains=search_value)
                    |
                Q(description__icontains=search_value)
            )

    context = {
        'games': games,
        'page_title': genre.name,
        'search_form': search_form,
    }

    return render(request, 'games/games_list.html', context)

def games_by_platform(request: HttpRequest, slug: str):
    platform = get_object_or_404(Platform, slug=slug)
    games = Game.objects.filter(platforms=platform)
    search_form = GameSearchForm(request.GET or None)

    if 'query' in request.GET:
        if search_form.is_valid():
            search_value = search_form.cleaned_data['query']
            games = games.filter(
                Q(name__icontains=search_value)
                    |
                Q(description__icontains=search_value)
            )

    context = {
        'games': games,
        'page_title': platform.name,
        'search_form': search_form,
    }

    return render(request, 'games/games_list.html', context)

def platforms_list(request: HttpRequest):
    list_platforms = Platform.objects.all().order_by('name')

    context = {
        'platforms': list_platforms,
        'page_title': 'All Platforms'
    }

    return render(request, 'games/platforms_list.html', context)

def add_game(request: HttpRequest):
    form = AddGameForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        game = form.save()
        return redirect('game_details', game_id=game.id)

    context = {
        'form': form,
        'action': 'add',
    }

    return render(request, 'games/game_form.html', {
        'form': form,
        'action': 'add',
        'cancel_url': reverse('games_list'),
    })

def edit_game(request: HttpRequest, game_id: str):
    game = get_object_or_404(Game, id=game_id)

    form = EditGameForm(request.POST or None, instance=game)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('games_list')

    return render(request, 'games/game_form.html', {
        'form': form,
        'action': 'edit',
        'cancel_url': game.get_absolute_url(),
    })

def delete_game(request: HttpRequest, game_id: str):
    game = get_object_or_404(Game, id=game_id)

    form = DeleteGameForm(request.POST or None, instance=game)

    for field in form.fields.values():
        field.disabled = True

    if request.method == 'POST':
        game.delete()
        return redirect('games_list')

    return render(request, 'games/game_form.html', {
        'form': form,
        'action': 'delete',
        'cancel_url': reverse('games_list'),
    })