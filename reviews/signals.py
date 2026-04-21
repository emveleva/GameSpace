from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review
from .tasks import send_review_notification_email

from celery.exceptions import OperationalError
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Review)
def review_created(sender, instance, created, **kwargs):
    if created:
        try:
            send_review_notification_email.delay(
                instance.game.id,
                instance.user.username,
                instance.rating
            )
        except OperationalError:
            logger.error("Celery/Redis not available - skipping email task")