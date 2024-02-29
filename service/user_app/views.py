from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from product_app.models import Product
from user_actions_app.permissions import IsAdminOrOwner
from .models import UserProductRelation, UserPostRelation

from .serializers import (UserProductRelationSerializer, UserProductRelationListSerializer,
                          UserPostRelationSerializer,)


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
        serializer.validated_data['user'] = self.request.user

        # if user do not have relation with product
        if not new_qs.exists():
            if serializer.validated_data['is_favorite']:
                return serializer.save()
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

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']: return UserProductRelationListSerializer
        return UserProductRelationSerializer


class UserPostRelationAPIView(viewsets.ModelViewSet):
    queryset = UserPostRelation.objects.all()
    serializer_class = UserPostRelationSerializer
    permission_classes = (IsAuthenticated, IsAdminOrOwner)

    def get_object(self):
        """
        It was difficult but I did it
        """
        from product_app.models import Product
        from .UserPostRelationService import UserPostRelationService
        from user_actions_app.models import Answer

        # checking if there is the product instance
        get_object_or_404(Product, pk=self.kwargs.get('product_pk'))

        # defining model
        parent_model, parent_pk = UserPostRelationService.define_instance_and_pk(self.kwargs)
        UserPostRelationService.validate_index(parent_pk)
        parent_qs = parent_model.objects.filter(product_id=self.kwargs.get('product_pk'))
        instance = UserPostRelationService.get_instance_by_pk(qs=parent_qs, pk=parent_pk)

        # if source is answer
        if self.kwargs.get('answer_pk') is not None:
            answer_pk = self.kwargs.get('answer_pk')-1
            UserPostRelationService.validate_index(answer_pk)
            instance = UserPostRelationService.get_instance_by_pk(instance.answer.all(), answer_pk)

        # recalculating rating

        return UserPostRelationService.relation_logic(instance=instance, grade=self.request.data.get('grade', 0),
                                                      user=self.request.user)
