from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.http import Http404

from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from product_app.models import Product
from user_actions_app.tasks import base_rating_counter
from .models import Question, Review, Answer
from .permissions import IsAdminOrOwner
from .serializers import (QuestionSerializer, QuestionPostSerializer, ReviewSerializer, AnswerCreateSerializer,
                          ReviewPostSerializer, AnswerGenericSerializer)

from .AnswerService import AnswerService
from .BaseProductPostService import BaseProductPostService


class BaseProductPostView(viewsets.ModelViewSet):
    """
    Base class for Review and Question
    models because they have same functional
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_ok = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if is_ok:
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({'detail': 'You already made Question/Review on this product.'})

    def perform_create(self, serializer):
        """
        Adding information to the serializer
        """
        product_id = self.kwargs.get('product_pk')

        if self.request.get_full_path().split('/')[-2] == 'reviews': current_model = Review
        else: current_model = Question

        try:
            get_object_or_404(current_model, author=self.request.user, product_id=product_id)
            return False
        except Http404:
            serializer.validated_data['product_id'] = product_id
            serializer.validated_data['author'] = self.request.user
            serializer.validated_data['rating'] = 0
            serializer.save()
            return True

    def get_permissions(self):
        """
        Checking if user has permissions
        """
        if self.request.method not in SAFE_METHODS:
            self.permission_classes = (IsAdminOrOwner, )
        else:
            self.permission_classes = ()

        return [permission() for permission in self.permission_classes]


class QuestionViewSet(BaseProductPostView):
    """
    Questions APIView
    """
    serializer_class = QuestionSerializer

    def get_object(self):
        return BaseProductPostService.get_object(queryset=self.get_queryset(), kwargs=self.kwargs, pk_='question_pk')

    def get_queryset(self):
        """
        Getting queryset
        """
        product_id = self.kwargs.get('product_pk')
        get_object_or_404(Product, pk=product_id)
        qs = BaseProductPostService.validate_queryset(
            qs=Question.objects.filter(product_id=product_id)
        )
        return qs

    def get_serializer_class(self):
        """
        Selecting proper serializer
        depends on request method
        """
        if self.action == 'create':
            return QuestionPostSerializer
        return QuestionSerializer


class ReviewViewSet(BaseProductPostView):
    """
    Review APIView
    """
    serializer_class = ReviewSerializer

    def get_object(self):
        return BaseProductPostService.get_object(queryset=self.get_queryset(), kwargs=self.kwargs, pk_='review_pk')

    def get_queryset(self):
        """
        Getting queryset
        """
        product_id = self.kwargs.get('product_pk')
        get_object_or_404(Product, pk=product_id)
        qs = BaseProductPostService.validate_queryset(
            qs=Review.objects.filter(product_id=product_id).prefetch_related(
                Prefetch('author', get_user_model().objects.all()
            ))
        )
        return qs

    def get_serializer_class(self):
        """
        Selecting proper serializer
        depends on request method
        """
        if self.action == 'create':
            return ReviewPostSerializer
        return ReviewSerializer

    def perform_destroy(self, instance):
        """
        Recalc ratings, solution with signal using is
        overcomplicated
        """
        instance_copy = instance
        instance.delete()
        base_rating_counter.delay(instance_copy.product_id)


class AnswerViewSet(viewsets.ModelViewSet):
    """
    Describes workflow behaviour with `Answer` model
    """
    serializer_class = AnswerGenericSerializer

    def get_object(self):
        """
        Gets each object of queryset
        with index equal path parameter <int:pk> that is
        """
        return AnswerService.get_object(queryset=self.get_queryset(), kwargs=self.kwargs)

    def get_queryset(self):
        """
        Getting each `Answer` instance
        related to the `Review` or `Question` model
        """
        obj, _ = AnswerService.get_source_instance(self.kwargs)
        qs = Answer.objects.all().prefetch_related(
            Prefetch('author', get_user_model().objects.all())
        )
        return [i for i in qs if i.content_object == obj]

    def get_serializer_class(self):
        """
        Gives the proper serializer class
        depends on the request method
        """
        if self.request.method == 'POST':
            return AnswerCreateSerializer
        return AnswerGenericSerializer

    def perform_create(self, serializer):
        """
        Adding values to the
        serializer class
        """
        obj, _ = AnswerService.get_source_instance(self.kwargs)

        serializer.validated_data['author'] = self.request.user
        serializer.validated_data['content_object'] = obj
        serializer.validated_data['object_id'] = obj.pk
        serializer.save()

    def get_permissions(self):
        """
        Checking if user is owner or admin
        if request method isn't safe
        """
        if self.request.method not in SAFE_METHODS:
            self.permission_classes = (IsAdminOrOwner, )
        else:
            self.permission_classes = ()
        return [permission() for permission in self.permission_classes]


@receiver(post_save, sender=Review)
def recalc_ratings_on_create(sender, instance, **kwargs):
    """for create"""
    base_rating_counter.delay(instance.product_id)


@receiver(pre_save, sender=Review)
def recalc_ratings_on_update(sender, instance, **kwargs):
    """for update"""
    base_rating_counter.delay(instance.product_id)
