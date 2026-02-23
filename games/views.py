from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from django.urls import reverse

from games.forms import AddGameForm, EditGameForm, DeleteGameForm
from games.models import Game, Genre, Platform


def games_list(request: HttpRequest):
    list_games = Game.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('name')

    context = {
        'games': list_games,
        'page_title': 'All Games'
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
    list_genres = Genre.objects.all().order_by('name')

    context = {
        'genres': list_genres,
        'page_title': 'All Genres'
    }

    return render(request, 'games/genres_list.html', context)

def games_by_genre(request: HttpRequest, slug: str):
    genre = get_object_or_404(Genre, slug=slug)
    games = Game.objects.filter(genres=genre)
    context = {
        'games': games,
        'page_title': genre.name,
    }

    return render(request, 'games/games_list.html', context)

def games_by_platform(request: HttpRequest, slug: str):
    platform = get_object_or_404(Platform, slug=slug)
    games = Game.objects.filter(platforms=platform)
    context = {
        'games': games,
        'page_title': platform.name,
    }

    return render(request, 'games/games_list.html', context)

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
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('games_list')

    return render(request, 'games/game_form.html', {
        'form': form,
        'action': 'edit',
        'cancel_url': reverse('game_details', args=[game.id]),
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