from django.http import Http404

from user_actions_app.models import Review, Question


class AnswerService:
    """
    Class that has required methods
    for the `Answer` model
    """
    @staticmethod
    def get_source_instance(kwargs):
        if 'review_pk' in kwargs.keys():
            index = kwargs['review_pk'] - 1
            current_model = Review
        else:
            index = kwargs['question_pk'] - 1
            current_model = Question

        obj = current_model.objects.filter(product_id=kwargs.get('product_pk'))[index]

        return obj, current_model

    @staticmethod
    def get_object(queryset, kwargs):
        pk = kwargs.get('pk')
        if pk < 1: raise Http404

        try:
            return queryset[pk-1]
        except IndexError:
            raise Http404
