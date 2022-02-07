import datetime
from rest_framework import serializers
from api.models import ParticipantAnswer, QuestionAnswer, Question, Quiz
from api.utils.participant_answers import update_participant_start_date


class QuestionAnswersParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = ["id", "answer"]


class QuestionParticipantParticipantSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    question = serializers.CharField(read_only=True)
    answers = QuestionAnswersParticipantSerializer(read_only=True, many=True)
    answer_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Question
        fields = ["id", "question", "answers", "answer_id"]

    def validate(self, data):

        # check time
        quiz_id = self.context["view"].kwargs.get("quiz_id")

        quiz = Quiz.objects.get(id=quiz_id)

        if quiz.datetime_limit is not None:
            if quiz.datetime_limit < datetime.datetime.now():
                raise serializers.ValidationError(
                    {"question": "the time to answer the quiz is over"}
                )

        question_id = self.context["view"].kwargs.get("pk")
        user = self.context.get("request").user
        participant_answer = ParticipantAnswer.objects.filter(
            quiz_id=quiz_id, question=question_id, user=user
        )

        if participant_answer:
            # if user already answer
            if participant_answer.first().answered_at is not None:
                raise serializers.ValidationError(
                    {"question": "already answered the question"}
                )

            if quiz.question_time_limit is not None:

                datetime_now_with_question_time = (
                    participant_answer.first().started_at
                    + datetime.timedelta(seconds=quiz.question_time_limit)
                )

                if datetime_now_with_question_time < datetime.datetime.now():
                    raise serializers.ValidationError(
                        {"question": "the time to answer this question is over"}
                    )

        # if user have not seen the question and answers yet
        else:
            if not update_participant_start_date(quiz_id, question_id, user):
                raise serializers.ValidationError(
                    {"error": ["question or quiz not found"]}
                )

        # validate answer id
        question_answer = QuestionAnswer.objects.filter(
            id=data["answer_id"], question_id=question_id
        )

        if not question_answer:
            raise serializers.ValidationError(
                {"answer_id": "answer_id does not exists"}
            )

        return data

    def create(self, validated_data):

        quiz_id = self.context["view"].kwargs.get("quiz_id")
        question_id = self.context["view"].kwargs.get("pk")
        user = self.context.get("request").user

        participant_answer = ParticipantAnswer.objects.filter(
            quiz_id=quiz_id, question=question_id, user=user
        )
        participant_answer.update(
            answer_id=validated_data["answer_id"], answered_at=datetime.datetime.now()
        )
        return participant_answer
