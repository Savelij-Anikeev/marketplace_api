from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import generics, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from product_app.models import Product
from .models import UserProductRelation, UserPostRelation

from .serializers import (UserProductRelationSerializer, UserProductRelationListSerializer,
                          UserPostRelationSerializer, UserSerializer, UserCreateSerializer,
                          UserUpdateSerializer)


class UserProductRelationAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProductRelation.objects.all()
    serializer_class = UserProductRelationSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        product = get_object_or_404(Product, id=self.kwargs.get('product_pk'))
        instance, _ = UserProductRelation.objects.get_or_create(product=product, user=self.request.user)
        return instance

    def perform_update(self, serializer):
        obj = self.get_object()
        if serializer.validated_data['is_favorite'] != True: obj.delete()
        else:
            obj.is_favorite = True
            obj.save()


class UserProductRelationList(generics.ListAPIView):
    queryset = UserProductRelation
    serializer_class = UserProductRelationListSerializer

    def get_queryset(self):
        qs = UserProductRelation.objects.filter(user=self.request.user)
        if qs.exists(): return qs
        raise Http404


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
