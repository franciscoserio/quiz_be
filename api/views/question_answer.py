from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from api.models import QuestionAnswer
from api.serializers.answer_serializers import AnswerSerializer


class ListCreateQuestionAnswerView(ListCreateAPIView):

    serializer_class = AnswerSerializer
    filterset_fields = ["answer"]

    def get_queryset(self):
        if self.request.user.is_admin:
            return QuestionAnswer.objects.filter(
                question__quiz_id=self.kwargs.get("quiz_id"),
                question__id=self.kwargs.get("question_id"),
            )
        return QuestionAnswer.objects.filter(
            question__quiz__user=self.request.user,
            question__quiz_id=self.kwargs.get("quiz_id"),
            question__id=self.kwargs.get("question_id"),
        )


class RetrieveUpdateDestroyQuestionAnswerView(RetrieveUpdateDestroyAPIView):

    serializer_class = AnswerSerializer

    def get_queryset(self):
        if self.request.user.is_admin:
            return QuestionAnswer.objects.filter(
                question__quiz_id=self.kwargs.get("quiz_id"),
                question__id=self.kwargs.get("question_id"),
            )
        return QuestionAnswer.objects.filter(
            question__quiz__user=self.request.user,
            question__quiz_id=self.kwargs.get("quiz_id"),
            question__id=self.kwargs.get("question_id"),
        )
