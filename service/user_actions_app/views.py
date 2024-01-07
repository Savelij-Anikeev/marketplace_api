from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from product_app.models import Product
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
    def get_object(self):
        """
        Getting proper object
        """
        return BaseProductPostService.get_object(queryset=self.get_queryset(), kwargs=self.kwargs)

    def perform_create(self, serializer):
        """
        Adding information to the serializer
        """
        # if product exits
        product_id = self.kwargs.get('product_pk')
        _ = get_object_or_404(Product, pk=product_id)

        # changing data
        serializer.validated_data['product_id'] = product_id
        serializer.validated_data['author'] = self.request.user
        serializer.validated_data['rating'] = 0
        serializer.save()

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

    def get_queryset(self):
        """
        Getting queryset
        """
        product_id = self.kwargs.get('product_pk')
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

    def get_queryset(self):
        """
        Getting queryset
        """
        product_id = self.kwargs.get('product_pk')
        qs = BaseProductPostService.validate_queryset(
            qs=Review.objects.filter(product_id=product_id)
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

    def perform_create(self, serializer):
        super().perform_create(serializer)


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
        return [i for i in Answer.objects.all() if i.content_object == obj]

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
        if self.request.method not in SAFE_METHODS:
            self.permission_classes = (IsAdminOrOwner, )
        else:
            self.permission_classes = ()
        return [permission() for permission in self.permission_classes]
