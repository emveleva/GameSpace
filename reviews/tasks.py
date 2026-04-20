from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Game

@shared_task
def send_review_notification_email(game_id, reviewer_username, rating):
    try:
        game = Game.objects.select_related("created_by").get(id=game_id)
        owner_email = game.created_by.email

        if not owner_email:
            return

        subject = f"New review for {game.name}"
        message = (
            f"Hi {game.created_by.username},\n\n"
            f"Your game '{game.name}' received a new review.\n"
            f"Reviewer: {reviewer_username}\n"
            f"Rating: {rating}\n"
        )

        send_mail(
            subject,
            message,
            "noreply@gamespace.com",
            [owner_email],
            fail_silently=False,
        )
    except Game.DoesNotExist:
        return