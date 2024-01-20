from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from static_app.models import Video, Image

"""
Base Models
"""

UserModel = get_user_model()


class BasePost(models.Model):

    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    rating = models.FloatField(null=True, blank=True, default=0, validators=(
                                MinValueValidator(0),
                                MaxValueValidator(5)))    # validators
    # review = GenericRelation('Review')  # p.review.all() - get each rel

    def __str__(self):
        return str(self.created)


class Question(BasePost, models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING)
    product_id = models.PositiveIntegerField()
    text = models.CharField(max_length=256)
    answer = GenericRelation('Answer')
    user_relation = GenericRelation('user_app.UserPostRelation')

    def __str__(self):
        return f'Question - {self.author} - {self.text}'


class Review(BasePost, models.Model):
    # DRY
    author = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING)
    product_id = models.PositiveIntegerField()
    text = models.CharField(max_length=256)
    answer = GenericRelation('Answer')
    photos = GenericRelation(Image)
    videos = GenericRelation(Video)
    grade = models.PositiveIntegerField()
    user_relation = GenericRelation('user_app.UserPostRelation')

    def __str__(self):
        return f'Review - {self.author} - {self.text}'


class Answer(BasePost, models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING)
    text = models.CharField(max_length=256)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    answer = GenericRelation('Answer')
    user_relation = GenericRelation('user_app.UserPostRelation')

    def __str__(self):
        return f'Answer - {self.author} - {self.text}'
