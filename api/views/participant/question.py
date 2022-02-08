from rest_framework.generics import CreateAPIView, RetrieveAPIView
from api.models import ParticipantAnswer, Question
from api.permissions import IsParticipant
from api.serializers.participant.participant_question_serializers import (
    QuestionParticipantParticipantSerializer,
)
from api.utils.participant_answers import update_participant_start_date
from rest_framework import serializers


class RetrieveQuestionAnswerParticipantQuizView(RetrieveAPIView):

    permission_classes = [IsParticipant]

    def get_serializer_class(self):

        # start time
        if not update_participant_start_date(
            self.kwargs.get("quiz_id"), self.kwargs.get("pk"), self.request.user
        ):
            raise serializers.ValidationError({"error": ["question or quiz not found"]})

        return QuestionParticipantParticipantSerializer

    def get_queryset(self):
        return Question.objects.filter(quiz__participants__user=self.request.user)


class CreateQuestionAnswerParticipantQuizView(CreateAPIView):

    permission_classes = [IsParticipant]
    serializer_class = QuestionParticipantParticipantSerializer

    def get_queryset(self):
        return ParticipantAnswer.objects.filter(
            user=self.request.user,
            quiz_id=self.kwargs.get("quiz_id"),
            question_id=self.kwargs.get("pk"),
        )
