from collections import defaultdict

from django.db.models.functions import Lower
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from games.models import Game
from genres.forms import AddGenreForm, EditGenreForm, DeleteGenreForm
from genres.models import Genre

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

    return render(request, 'genres/genres_list.html', context)


def genre_details(request: HttpRequest, slug: str):
    genre = get_object_or_404(Genre, slug=slug)

    games = Game.objects.filter(genres=genre).order_by('name')

    context = {
        'genre': genre,
        'games': games,
    }
    return render(request, 'genres/genre_details.html', context)

def add_genre(request: HttpRequest):
    form = AddGenreForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        genre = form.save()
        return redirect('genre_details', slug=genre.slug)

    return render(request, 'genres/genre_form.html', {
        'form': form,
        'action': 'add',
        'cancel_url': reverse('genres_list'),
    })

def edit_genre(request: HttpRequest, slug: str):
    genre = get_object_or_404(Genre, slug=slug)

    form = EditGenreForm(request.POST or None, instance=genre)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('genres_list')

    return render(request, 'genres/genre_form.html', {
        'form': form,
        'action': 'edit',
        'cancel_url': genre.get_absolute_url(),
    })

def delete_genre(request: HttpRequest, slug: str):
    genre = get_object_or_404(Genre, slug=slug)

    form = DeleteGenreForm(request.POST or None, instance=genre)

    for field in form.fields.values():
        field.disabled = True

    if request.method == 'POST':
        genre.delete()
        return redirect('genres_list')

    return render(request, 'genres/genre_form.html', {
        'form': form,
        'action': 'delete',
        'cancel_url': reverse('genres_list'),
    })