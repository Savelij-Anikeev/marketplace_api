from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import UserPostRelation
from .tasks import recalculate_rating


@receiver(post_save, sender=UserPostRelation)
def recalculate_rating_on_create(instance, *args, **kwargs):
    recalculate_rating.delay(instance=instance)


@receiver(pre_save, sender=UserPostRelation)
def recalculate_rating_on_create(instance, *args, **kwargs):
    recalculate_rating.delay(instance=instance)




