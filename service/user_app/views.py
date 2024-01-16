from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import generics, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from product_app.models import Product
from .models import UserProductRelation, UserPostRelation, User

from .serializers import (UserProductRelationSerializer, UserProductRelationListSerializer,
                          UserPostRelationSerializer, UserSerializer, UserCreateSerializer,
                          UserUpdateSerializer)


class UserProductRelationViewSet(viewsets.ModelViewSet):
    queryset = UserPostRelation.objects.all().prefetch_related('user')
    serializer_class = UserProductRelationSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        """
        Letting user retrieve UserProductRelation instance
        using product pk, to make API more user-friendly
        """
        product = get_object_or_404(Product, id=self.kwargs.get('pk'))
        instance, _ = UserProductRelation.objects.get_or_create(product=product, user=self.request.user)
        return instance

    def perform_create(self, serializer):
        """
        Checking if user already have relation
        with product
        """
        qs = self.get_queryset()
        product = serializer.validated_data['product']
        new_qs = qs.filter(user=self.request.user, product=product)

        # if user do not have relation with product
        if not new_qs.exists():
            serializer.save()
            return

        # checking if we should delete relation
        # cause of `is_favorite` == False
        if serializer.validated_data['is_favorite']:
            new_qs[0].is_favorite = serializer.validated_data['is_favorite']
            new_qs[0].save()
        else:
            new_qs[0].delete()

    def perform_update(self, serializer):
        """
        Deleting relation when
        user changes `is_favorite` with False
        to not fill database with useless data
        """
        obj = self.get_object()
        if not serializer.validated_data['is_favorite']: obj.delete()
        else:
            obj.is_favorite = True
            obj.save()

    def get_queryset(self):
        """
        Getting relations that are
        only related with the current user
        """
        qs = UserProductRelation.objects.filter(user=self.request.user).prefetch_related('user')
        return qs


class UserPostRelationAPIView(viewsets.ModelViewSet):
    queryset = UserPostRelation.objects.all()
    serializer_class = UserPostRelationSerializer
    permission_classes = (IsAuthenticated, )

    # def get_object(self):
    #     from product_app.models import Product
    #     from user_actions_app.models import Review, Question, Answer
    #
    #     product = get_object_or_404(Product, pk=self.kwargs.get('product_pk'))  # product instance

        ## defining model
        # if self.kwargs.get('review_pk') is not None:
        #     parent_pk = self.kwargs.get('review_pk') - 1
        #     parent_model = Review
        # else:
        #     parent_pk = self.kwargs.get('question_pk') - 1
        #     parent_model = Question

        ## queryset doesn't support negative indexes
        # if parent_pk < 0:
        #     return Http404

        ## if index too big
        # try:
        #     parent_object = parent_model.objects.filter(product_id=product.pk)[parent_pk]
        # except IndexError:
        #     raise Http404

        ## if self.kwargs.get('answer_pk') is None:
        # target = parent_object
        # obj, _ = UserPostRelation.objects.get_or_create(object_id=target.pk,
        #                                                 post=target,
        #                                                 user=self.request.user,
        #                                                 grade=1)
        # parent_object = Review.objects.filter(product_id=product.pk)[0]
        # obj = UserPostRelation.objects.create(object_id=parent_object.pk,
        #                                                 post=parent_object,
        #                                                  user=self.request.user,
        #                                                  grade=1)
        # obj.save()
        # return obj


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    permission_classes = (IsAdminUser,)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ('update', 'partial_update'):
            return UserUpdateSerializer
        return UserSerializer
