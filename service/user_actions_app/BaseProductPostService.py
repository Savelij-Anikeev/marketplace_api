from django.http import Http404


class BaseProductPostService:
    """
    Class that has required methods
    for the `BaseProductPost` View
    """
    @staticmethod
    def get_object(queryset, kwargs, pk_):
        pk = kwargs.get(pk_)
        if pk < 1: raise Http404

        try:
            return queryset[pk-1]
        except IndexError:
            raise Http404

    @staticmethod
    def validate_queryset(qs):
        """
        Checking if qs is empty
        """
        if qs.exists(): return qs
        raise Http404

    # for serializer
    @staticmethod
    def check_static(validated_data):
        uploaded_images = uploaded_videos = None

        if validated_data.get("uploaded_images") is not None:
            uploaded_images = validated_data.pop("uploaded_images")
        if validated_data.get("uploaded_videos") is not None:
            uploaded_videos = validated_data.pop("uploaded_videos")

        return uploaded_images, uploaded_videos

    @staticmethod
    def give_static(uploaded_images, uploaded_videos, instance):
        from static_app.models import Image, Video

        if uploaded_images:
            for img in uploaded_images:
                Image.objects.create(content_object=instance, object_id=instance.pk, url=img)

        if uploaded_videos:
            for vid in uploaded_videos:
                Video.objects.create(content_object=instance, object_id=instance.pk, url=vid)

    @staticmethod
    def check_if_there_is_instance(current_model, user, product_id):
        q = current_model.objects.filter(author=user, product_id=product_id)
        return not q.count() > 0
