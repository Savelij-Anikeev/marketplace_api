from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class User(AbstractUser):
    ROLES = [
        ("default", "default"),
        ("vendor_staff", "vendor_staff"),
        ("vendor_manager", "vendor_manager"),
    ]
    photo = models.ImageField(null=True, blank=True)
    phone = models.CharField(max_length=16, null=True, blank=True)  # set null=False, it is required
    balance = models.PositiveIntegerField(default=0)
    email = models.EmailField(unique=True)

    work_place = models.ForeignKey('vendor_app.Vendor', on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=24, choices=ROLES, default=ROLES[0][0])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class UserProductRelation(models.Model):
    """
    Created to represent relation
    between product and user
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey('product_app.Product', on_delete=models.CASCADE)
    is_favorite = models.BooleanField(default=False)


class UserPostRelation(models.Model):
    """
    Created to represent relation
    between post (review, question, answer) and user
    """
    GRADE_CHOICES = [
        (1, 1),
        (0, 0),
        (-1, -1),
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    grade = models.IntegerField(choices=GRADE_CHOICES, default=GRADE_CHOICES[1][0])

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    post = GenericForeignKey('content_type', 'object_id')
