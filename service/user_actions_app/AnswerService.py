from django.http import Http404

from user_actions_app.models import Review, Question


class AnswerService:
    """
    Class that has required methods
    for the `Answer` model
    """
    @staticmethod
    def get_source_instance(kwargs):
        current_model = None
        if 'review_pk' in kwargs.keys():
            obj = Review.objects.filter(product_id=kwargs.get('product_pk'))[kwargs['review_pk'] - 1]
            current_model = Review
        else:
            obj = Question.objects.filter(product_id=kwargs.get('product_pk'))[kwargs['question_pk'] - 1]
            current_model = Question

        return obj, current_model

    @staticmethod
    def get_object(queryset, kwargs):
        pk = kwargs.get('pk')
        if pk < 1: raise Http404

        try:
            return queryset[pk-1]
        except IndexError:
            raise Http404
