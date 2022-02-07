from rest_framework import serializers
from api.models import Quiz
from api.utils.status import calculate_time_left, questions_answered, questions_left


class QuizStatusParticipantSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    question_time_limit = serializers.IntegerField(required=False)
    datetime_limit = serializers.DateTimeField(required=False)

    class Meta:
        model = Quiz
        fields = ["id", "name", "description", "question_time_limit", "datetime_limit"]

    def to_representation(self, instance):
        data = super(QuizStatusParticipantSerializer, self).to_representation(instance)
        response = dict()
        response["datetime_limit"] = data["datetime_limit"]
        response["time_left"] = calculate_time_left(data["datetime_limit"])
        response["questions_answered"] = questions_answered(
            self.context["view"].kwargs.get("pk"), self.context.get("request").user
        )
        response["questions_left"] = questions_left(
            self.context["view"].kwargs.get("pk"), self.context.get("request").user
        )
        return response
