from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from api.models import Question
from api.serializers.question_serializers import QuestionSerializer


class ListCreateQuestionView(ListCreateAPIView):

    serializer_class = QuestionSerializer
    filterset_fields = ["question"]

    def get_queryset(self):
        if self.request.user.is_admin:
            return Question.objects.filter(quiz_id=self.kwargs.get("quiz_id"))
        return Question.objects.filter(
            quiz__user=self.request.user, quiz_id=self.kwargs.get("quiz_id")
        )


class RetrieveUpdateDestroyQuestionView(RetrieveUpdateDestroyAPIView):

    serializer_class = QuestionSerializer

    def get_queryset(self):
        if self.request.user.is_admin:
            return Question.objects.filter(quiz_id=self.kwargs.get("quiz_id"))
        return Question.objects.filter(
            quiz__user=self.request.user, quiz_id=self.kwargs.get("quiz_id")
        )
