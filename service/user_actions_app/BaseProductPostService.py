from django.http import Http404


class BaseProductPostService:
    """
    Class that has required methods
    for the `BaseProductPost` View
    """
    @staticmethod
    def get_object(queryset, kwargs):
        pk = kwargs.get('pk')
        if pk < 1: raise Http404

        try:
            return queryset[pk-1]
        except IndexError:
            raise Http404

    @staticmethod
    def validate_queryset(qs):
        """
        Checkign if qs is empty
        """
        if qs.exists(): return qs
        raise Http404
