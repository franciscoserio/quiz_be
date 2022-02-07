from rest_framework.generics import ListAPIView, RetrieveAPIView
from api.models import Quiz
from api.permissions import IsParticipant
from api.serializers.participant.participant_quiz_serializers import (
    ParticipantQuizSerializer,
)
from api.serializers.quiz_serializers import QuizSerializer


class ListParticipantQuizView(ListAPIView):

    permission_classes = [IsParticipant]
    serializer_class = QuizSerializer

    def get_queryset(self):
        return Quiz.objects.filter(participants__user=self.request.user)


class RetrieveParticipantQuizView(RetrieveAPIView):

    permission_classes = [IsParticipant]
    serializer_class = ParticipantQuizSerializer

    def get_queryset(self):
        return Quiz.objects.filter(participants__user=self.request.user)
