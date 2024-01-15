import json

from rest_framework import serializers

from static_app.serializers import ImageSerializer, VideoSerializer
from .BaseProductPostService import BaseProductPostService
from .models import Question, Review, Answer

from user_app.serializers import UserAnswerSerializer


# Serializers for answer model
class AnswerGenericSerializer(serializers.ModelSerializer):
    author = UserAnswerSerializer()
    text = serializers.StringRelatedField()

    class Meta:
        model = Answer
        fields = ('author', 'text', 'rating', 'created', 'updated')


class AnswerSerializer(serializers.ModelSerializer):
    """
    Main serializer
    """
    answer = serializers.SerializerMethodField()
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Answer
        fields = ('id', 'author', 'text', 'answer')

    def get_answer(self, obj):
        d = []
        for i in obj.answer.all():
            d.append(json.dumps(i))
        return d


class AnswerCreateSerializer(serializers.ModelSerializer):
    """
    Used for POST requests
    """
    content_object = serializers.StringRelatedField()

    class Meta:
        model = Answer
        fields = ('text', 'content_object')


# Serializers for question model
class QuestionSerializer(serializers.ModelSerializer):
    """
    Main serializer
    """
    author = UserAnswerSerializer()
    answer = AnswerGenericSerializer(many=True)

    class Meta:
        model = Question
        fields = ('author', 'text', 'rating', 'created', 'updated', 'answer')
        read_only_fields = ('product_id', 'rating')


class QuestionPostSerializer(serializers.ModelSerializer):
    """
    Used for POST requests
    """
    class Meta:
        model = Question
        fields = ('text',)
        read_only_fields = ('author', 'product_id', 'rating', 'created', 'updated')


# Serializers for Review model
class ReviewSerializer(serializers.ModelSerializer):
    """
    Main review serializer
    """
    author = UserAnswerSerializer(required=False, read_only=True)
    answer = AnswerGenericSerializer(many=True, required=False, read_only=True)
    photos = ImageSerializer(many=True, required=False)
    videos = VideoSerializer(many=True, required=False)

    class Meta:
        model = Review
        fields = ('author', 'text', 'photos', 'grade', 'videos', 'rating', 'created', 'updated', 'answer')
        read_only_fields = ('product_id', 'rating', 'answer')


class ReviewPostSerializer(serializers.ModelSerializer):
    """
    Used for POST requests
    """
    photos = ImageSerializer(read_only=True, many=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    videos = VideoSerializer(read_only=True, many=True)
    uploaded_videos = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Review
        fields = ('text', 'grade', 'photos', 'videos', 'uploaded_images', 'uploaded_videos')
        read_only_fields = ('author', 'product_id', 'rating', 'created', 'updated')

    def create(self, validated_data):
        #   //// DRY ////
        uploaded_images, uploaded_videos = BaseProductPostService.check_static(validated_data)
        review = super().create(validated_data)
        BaseProductPostService.give_static(uploaded_images, uploaded_videos, review)

        return review
