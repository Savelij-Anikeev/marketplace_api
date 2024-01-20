from django.http import Http404

from .tasks import recalculate_rating


class UserPostRelationService:
    @staticmethod
    def relation_logic(instance, user, grade):
        """
        I don't know how does it work, but it does
        """
        qs = instance.user_relation.all().filter(user=user)
        if qs.exists():
            if qs[0].object_id is None:
                qs[0].delete()
            else:
                recalculate_rating.delay(instance.pk, instance.__class__.__name__)
                return qs[0]
        recalculate_rating.delay(instance.pk, instance.__class__.__name__)
        return instance.user_relation.all().create(post=instance, user=user, object_id=instance.pk, grade=grade)

    @staticmethod
    def define_instance_and_pk(kwg: dict):
        """
        Helps to define model and pk
        """
        from user_actions_app.models import Question, Review

        if kwg.get('review_pk') is not None:
            parent_pk = kwg.get('review_pk') - 1
            parent_model = Review
        else:
            parent_pk = kwg.get('question_pk') - 1
            parent_model = Question

        return parent_model, parent_pk

    @staticmethod
    def validate_index(pk: int) -> None:
        """
        Validating index
        """
        if pk < 0:
            raise Http404

    @staticmethod
    def get_instance_by_pk(qs, pk: int) -> None:
        """
        Get instance by pk
        """
        try:
            return qs[pk]
        except IndexError:
            raise Http404
