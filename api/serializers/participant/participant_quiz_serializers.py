from rest_framework import serializers
from api.models import Quiz


class QuestionParticipantSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Quiz
        fields = ["id"]


class ParticipantQuizSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    question_time_limit = serializers.IntegerField(required=False)
    datetime_limit = serializers.DateTimeField(required=False)
    questions = QuestionParticipantSerializer

    class Meta:
        model = Quiz
        fields = [
            "id",
            "name",
            "description",
            "question_time_limit",
            "datetime_limit",
            "questions",
        ]
