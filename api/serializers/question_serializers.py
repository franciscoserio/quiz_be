from rest_framework import serializers
from api.models import Question
from api.serializers.answer_serializers import AnswerSerializer


class QuestionSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    answers = AnswerSerializer(read_only=True, many=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Question
        fields = ["id", "question", "created_at", "answers"]

    def validate(self, data):

        question = Question.objects.filter(question=data["question"])

        if question:
            raise serializers.ValidationError({"question": "question already exists"})

        return data

    def create(self, validated_data):

        validated_data["quiz_id"] = self.context["view"].kwargs.get("quiz_id")

        return Question.objects.create(**validated_data)
