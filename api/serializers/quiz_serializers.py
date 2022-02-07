import datetime
from rest_framework import serializers
from api.models import Quiz
from api.utils.results import participants_results, send_participants_results
from api.utils.status import calculate_time_left, total_questions_answered


class QuizSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    question_time_limit = serializers.IntegerField(required=False)
    datetime_limit = serializers.DateTimeField(required=False)

    class Meta:
        model = Quiz
        fields = ["id", "name", "description", "question_time_limit", "datetime_limit"]

    def create(self, validated_data):

        validated_data["user"] = self.context.get("request").user

        return Quiz.objects.create(**validated_data)


class QuizStatusSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    question_time_limit = serializers.IntegerField(required=False)
    datetime_limit = serializers.DateTimeField(required=False)

    class Meta:
        model = Quiz
        fields = ["id", "name", "description", "question_time_limit", "datetime_limit"]

    def to_representation(self, instance):
        data = super(QuizStatusSerializer, self).to_representation(instance)
        response = dict()
        response["datetime_limit"] = data["datetime_limit"]
        response["time_left"] = calculate_time_left(data["datetime_limit"])
        response["progress_total_questions_answered"] = total_questions_answered(
            self.context["view"].kwargs.get("pk")
        )
        return response


class QuizResultsSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    question_time_limit = serializers.IntegerField(required=False)
    datetime_limit = serializers.DateTimeField(required=False)

    class Meta:
        model = Quiz
        fields = ["id", "name", "description", "question_time_limit", "datetime_limit"]

    def to_representation(self, instance):
        data = super(QuizResultsSerializer, self).to_representation(instance)
        response = dict()

        response["participants"] = participants_results(
            self.context["view"].kwargs.get("pk")
        )
        return response


class NotifyQuizResultsSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    question_time_limit = serializers.IntegerField(required=False)
    datetime_limit = serializers.DateTimeField(required=False)

    class Meta:
        model = Quiz
        fields = ["id", "name", "description", "question_time_limit", "datetime_limit"]

    def to_representation(self, instance):
        data = super(NotifyQuizResultsSerializer, self).to_representation(instance)
        response = dict()

        quiz = Quiz.objects.get(id=self.context["view"].kwargs.get("pk"))
        if quiz.datetime_limit is not None:
            if quiz.datetime_limit > datetime.datetime.now():
                raise serializers.ValidationError(
                    {"quiz": "the time to answer the quiz is not over yet"}
                )

        # send results via email
        send_participants_results(self.context["view"].kwargs.get("pk"))

        response["results"] = "results were sent successfully via email"
        return response
