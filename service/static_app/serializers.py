from rest_framework import serializers

from .models import Image, Video


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('url', )


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('url', )
