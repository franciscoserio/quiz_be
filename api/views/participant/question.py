from rest_framework.generics import ListCreateAPIView
from api.models import ParticipantAnswer, Question
from api.permissions import IsParticipant
from api.serializers.participant.participant_question_serializers import (
    QuestionParticipantParticipantSerializer,
)
from api.utils.participant_answers import update_participant_start_date
from rest_framework import serializers


class QuestionParticipantQuizView(ListCreateAPIView):

    permission_classes = [IsParticipant]

    def get_serializer_class(self):

        if self.request.method == "GET":
            # start time
            if not update_participant_start_date(
                self.kwargs.get("quiz_id"), self.kwargs.get("pk"), self.request.user
            ):
                raise serializers.ValidationError(
                    {"error": ["question or quiz not found"]}
                )

        return QuestionParticipantParticipantSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return Question.objects.filter(quiz__participants__user=self.request.user)
        else:
            return ParticipantAnswer.objects.filter(
                user=self.request.user,
                quiz_id=self.kwargs.get("quiz_id"),
                question_id=self.kwargs.get("pk"),
            )
