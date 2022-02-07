from rest_framework import serializers
from api.models import QuestionAnswer


class AnswerSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = QuestionAnswer
        fields = ["id", "answer", "is_correct"]

    def validate(self, data):

        # validate more than one correct answers
        if ("is_correct" in data and data["is_correct"]) or ("is_correct" not in data):
            answers = QuestionAnswer.objects.filter(
                question_id=self.context["view"].kwargs.get("question_id"),
                is_correct=True,
            )

            if answers:
                raise serializers.ValidationError(
                    {"answer": "there is already an answer with a correct response"}
                )

        # validate same multiple answers
        if "answer" in data:
            answers = QuestionAnswer.objects.filter(
                question_id=self.context["view"].kwargs.get("question_id"),
                answer=data["answer"],
            )

            if answers:
                raise serializers.ValidationError(
                    {"answer": "there is already that answer"}
                )

        return data

    def create(self, validated_data):

        validated_data["question_id"] = self.context["view"].kwargs.get("question_id")

        return QuestionAnswer.objects.create(**validated_data)
