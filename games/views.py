from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from games.models import Game

def games_list(request):
    list_games = Game.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('name')

    context = {
        'games': list_games,
        'page_title': 'All Games'
    }

    return render(request, 'games_list.html', context)

def game_details(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    # average rating
    avg_rating = game.reviews.aggregate(Avg('rating'))['rating__avg']

    context = {
        'game': game,
        'avg_rating': avg_rating,
    }
    return render(request, 'game_details.html', context)