from rest_framework import serializers

from .models import User


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'photo', 'username')
