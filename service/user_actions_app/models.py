from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from static_app.models import Image

"""
Base Models
"""

UserModel = get_user_model()


class BasePost(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    rating = models.PositiveIntegerField(null=True, blank=True, default=0)    # validators
    # review = GenericRelation('Review')  # p.review.all() - get each rel

    def __str__(self):
        return str(self.created)


class Question(BasePost, models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING)
    product_id = models.PositiveIntegerField()
    text = models.CharField(max_length=256)
    answer = GenericRelation('Answer')

    def __str__(self):
        return f'Question - {self.author} - {self.text}'


class Review(BasePost, models.Model):
    # DRY
    author = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING)  #
    product_id = models.PositiveIntegerField()  #
    text = models.CharField(max_length=256)  #
    answer = GenericRelation('Answer')  #
    # photo = models.ImageField(null=True, blank=True)
    photos = GenericRelation(Image)

    def __str__(self):
        return f'Review - {self.author} - {self.text}'


class Answer(BasePost, models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING)
    text = models.CharField(max_length=256)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    answer = GenericRelation('Answer')

    def __str__(self):
        return f'Answer - {self.author} - {self.text}'
