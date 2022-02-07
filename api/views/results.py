from rest_framework.generics import RetrieveAPIView
from api.models import Quiz
from api.serializers.quiz_serializers import (
    QuizResultsSerializer,
    NotifyQuizResultsSerializer,
)


class ResultsQuizView(RetrieveAPIView):

    serializer_class = QuizResultsSerializer

    def get_queryset(self):
        if self.request.user.is_admin:
            return Quiz.objects.all()
        return Quiz.objects.filter(id=self.kwargs.get("pk"), user=self.request.user)


class NotifyResultsQuizView(RetrieveAPIView):

    serializer_class = NotifyQuizResultsSerializer

    def get_queryset(self):
        if self.request.user.is_admin:
            return Quiz.objects.all()
        return Quiz.objects.filter(id=self.kwargs.get("pk"), user=self.request.user)
