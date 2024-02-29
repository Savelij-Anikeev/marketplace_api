import time

from celery import shared_task
from django.db.models import Sum
from django.apps import apps


@shared_task
def recalculate_rating(instance_pk, instance_model):
    model = apps.get_model('user_actions_app', instance_model)
    instance = model.objects.get(pk=instance_pk)
    instance.rating = instance.user_relation.all().aggregate(Sum('grade')).get('grade__sum')
    instance.save()
