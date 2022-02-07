from rest_framework.generics import RetrieveAPIView
from api.models import Quiz
from api.permissions import IsParticipant
from api.serializers.participant.participant_quiz_status_serializers import (
    QuizStatusParticipantSerializer,
)


class StatusQuizParticipantView(RetrieveAPIView):

    permission_classes = [IsParticipant]
    serializer_class = QuizStatusParticipantSerializer

    def get_queryset(self):
        if self.request.user.is_admin:
            return Quiz.objects.all()
        return Quiz.objects.filter(id=self.kwargs.get("pk"))
